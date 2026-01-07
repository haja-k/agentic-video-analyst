"""
Orchestrator Agent - Routes queries to appropriate specialized agents
Uses Llama 3.1 8B to understand user intent and coordinate agent execution
"""
from typing import Dict, Any, List, Optional
import logging
from pathlib import Path
import json

from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class OrchestratorAgent(BaseAgent):
    """
    Main orchestrator that uses Llama 3.1 8B to:
    - Understand user queries
    - Route to appropriate agents
    - Coordinate multi-agent workflows
    - Generate final responses
    """
    
    def __init__(self, model_path: str, transcription_agent=None, 
                 vision_agent=None, generation_agent=None):
        super().__init__("Orchestrator", model_path)
        self.llm = None
        self.transcription_agent = transcription_agent
        self.vision_agent = vision_agent
        self.generation_agent = generation_agent
        self.conversation_history = []
        
    async def initialize(self):
        """Initialize Llama model for orchestration"""
        try:
            from llama_cpp import Llama
            
            logger.info(f"Loading Llama orchestrator model...")
            self.llm = Llama(
                model_path=self.model_path,
                n_ctx=4096,
                n_threads=6,
                n_gpu_layers=1,
                verbose=False
            )
            logger.info("Orchestrator model loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load orchestrator model: {e}")
            raise
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process user query and route to appropriate agents
        
        Args:
            input_data: {
                "query": str,
                "video_path": Optional[str],
                "context": Optional[Dict] (previous results, transcription, etc)
            }
            
        Returns:
            {
                "response": str,
                "actions_taken": List[str],
                "results": Dict (agent results),
                "requires_clarification": bool
            }
        """
        query = input_data.get("query", "")
        video_path = input_data.get("video_path")
        context = input_data.get("context", {})
        
        logger.info(f"Processing query: {query[:100]}...")
        
        intent = await self.analyze_intent(query, context)
        
        # Ensure intent has required keys
        if not intent or not isinstance(intent, dict):
            intent = self._parse_intent_from_text(query, context)
        
        if not intent.get("primary_action"):
            intent["primary_action"] = "respond"
        
        logger.info(f"Detected intent: {intent['primary_action']}")
        
        if intent.get("needs_clarification"):
            return {
                "response": intent["clarification_question"],
                "requires_clarification": True,
                "actions_taken": []
            }
        
        results = await self.execute_actions(intent, video_path, context)
        
        response = await self.generate_response(query, intent, results, context)
        
        # Build list of actions actually executed
        actions_executed = []
        if "transcription" in results:
            actions_executed.append("transcribe")
        if "vision" in results:
            actions_executed.append("vision_analysis")
        if "pdf" in results:
            actions_executed.append("generate_pdf")
        if "pptx" in results:
            actions_executed.append("generate_pptx")
        if "summary" in results:
            actions_executed.append("summarize")
        
        return {
            "response": response,
            "actions_taken": actions_executed,
            "results": results,
            "requires_clarification": False
        }
    
    async def analyze_intent(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Use Llama to analyze user intent and determine required actions
        """
        
        available_actions = """
        - transcribe: Extract speech-to-text from video
        - detect_objects: Find and identify objects in video frames
        - describe_scenes: Generate natural language descriptions of video content
        - analyze_graphs: Detect and describe charts/graphs in video
        - generate_pdf: Create PDF report from analysis
        - generate_pptx: Create PowerPoint presentation
        - summarize: Summarize previous analysis or conversation
        """
        
        has_transcription = bool(context.get("transcription"))
        has_vision = bool(context.get("vision_results"))
        
        system_prompt = f"""You are an AI assistant analyzing user queries about video content.
Your task is to determine what actions are needed to answer the query.

Available actions:
{available_actions}

Current context:
- Transcription available: {has_transcription}
- Vision analysis available: {has_vision}

Based on the user query, respond with a JSON object containing:
{{
    "primary_action": "action_name",
    "additional_actions": ["action1", "action2"],
    "needs_clarification": false,
    "clarification_question": "",
    "reasoning": "brief explanation"
}}

If the query is ambiguous, set needs_clarification to true and provide a clarification question.
If no new actions needed (just answering from context), set primary_action to "respond".

User query: {query}"""

        try:
            response = self.llm(
                system_prompt,
                max_tokens=256,
                temperature=0.3,
                stop=["User:", "\n\n\n"],
                echo=False
            )
            
            response_text = response['choices'][0]['text'].strip()
            
            # Try to extract JSON from response
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            if start != -1 and end > start:
                try:
                    intent_json = json.loads(response_text[start:end])
                    # Validate required keys
                    if "primary_action" in intent_json:
                        return intent_json
                except json.JSONDecodeError:
                    pass
            
            # Fallback: parse from text
            logger.info("LLM output not valid JSON, using keyword fallback")
            return self._parse_intent_from_text(query, context)
            
        except Exception as e:
            logger.warning(f"Intent analysis failed, using fallback: {e}")
            return self._parse_intent_from_text(query, context)
    
    def _parse_intent_from_text(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback intent parser using simple keyword matching"""
        query_lower = query.lower()
        
        intent = {
            "primary_action": "respond",
            "additional_actions": [],
            "needs_clarification": False,
            "clarification_question": "",
            "reasoning": "keyword-based fallback"
        }
        
        # Check for transcription requests
        if any(word in query_lower for word in ["transcribe", "transcript", "what was said", "speech", "audio"]):
            intent["primary_action"] = "transcribe"
            
        # Check for object detection
        elif any(word in query_lower for word in ["object", "detect", "identify", "what do you see", "items"]):
            intent["primary_action"] = "detect_objects"
            
        # Check for scene description
        elif any(word in query_lower for word in ["describe", "scene", "what's happening", "visual", "show"]):
            intent["primary_action"] = "describe_scenes"
            
        # Check for graph analysis
        elif any(word in query_lower for word in ["graph", "chart", "plot", "diagram"]):
            intent["primary_action"] = "detect_objects"
            intent["additional_actions"] = ["describe_scenes"]
            
        # Check for report generation
        elif "pdf" in query_lower or "report" in query_lower:
            intent["primary_action"] = "generate_pdf"
            if not context.get("transcription") or not context.get("vision_results"):
                intent["needs_clarification"] = True
                intent["clarification_question"] = "I'll need to analyze the video first. Should I transcribe and analyze it before generating the report?"
                
        elif "powerpoint" in query_lower or "pptx" in query_lower or "presentation" in query_lower:
            intent["primary_action"] = "generate_pptx"
            if not context.get("transcription") or not context.get("vision_results"):
                intent["needs_clarification"] = True
                intent["clarification_question"] = "I'll need to analyze the video first. Should I transcribe and analyze it before creating the presentation?"
                
        # Check for summary - improved matching
        elif any(word in query_lower for word in ["summary", "summarize", "summarise", "overview", "recap"]):
            intent["primary_action"] = "summarize"
        
        return intent
    
    async def execute_actions(self, intent: Dict[str, Any], 
                            video_path: Optional[str],
                            context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the actions determined by intent analysis"""
        results = {}
        actions = [intent["primary_action"]] + intent.get("additional_actions", [])
        
        for action in actions:
            try:
                if action == "transcribe" and self.transcription_agent:
                    if not video_path:
                        results["transcribe"] = {"error": "No video provided"}
                        continue
                    
                    logger.info("Executing transcription...")
                    transcription_result = await self.transcription_agent.process({
                        "video_path": video_path
                    })
                    results["transcription"] = transcription_result
                    context["transcription"] = transcription_result
                    
                elif action == "detect_objects" and self.vision_agent:
                    if not video_path:
                        results["detect_objects"] = {"error": "No video provided"}
                        continue
                    
                    logger.info("Executing object detection...")
                    vision_result = await self.vision_agent.process({
                        "video_path": video_path,
                        "task": "detect_objects",
                        "num_frames": 5
                    })
                    results["vision"] = vision_result
                    context["vision_results"] = vision_result
                    
                elif action == "describe_scenes" and self.vision_agent:
                    if not video_path:
                        results["describe_scenes"] = {"error": "No video provided"}
                        continue
                    
                    logger.info("Executing scene description...")
                    vision_result = await self.vision_agent.process({
                        "video_path": video_path,
                        "task": "describe_scene",
                        "num_frames": 5
                    })
                    results["vision"] = vision_result
                    context["vision_results"] = vision_result
                    
                elif action == "generate_pdf" and self.generation_agent:
                    logger.info("Generating PDF report...")
                    pdf_result = await self.generation_agent.process({
                        "format": "pdf",
                        "title": "Video Analysis Report",
                        "transcription": context.get("transcription"),
                        "vision_results": context.get("vision_results"),
                        "summary": context.get("summary", "")
                    })
                    results["pdf"] = pdf_result
                    
                elif action == "generate_pptx" and self.generation_agent:
                    logger.info("Generating PowerPoint presentation...")
                    pptx_result = await self.generation_agent.process({
                        "format": "pptx",
                        "title": "Video Analysis Presentation",
                        "transcription": context.get("transcription"),
                        "vision_results": context.get("vision_results"),
                        "summary": context.get("summary", "")
                    })
                    results["pptx"] = pptx_result
                    
                elif action == "summarize":
                    logger.info("Generating summary...")
                    summary = await self.generate_summary(context)
                    results["summary"] = summary
                    context["summary"] = summary
                    
            except Exception as e:
                logger.error(f"Action {action} failed: {e}")
                results[action] = {"error": str(e)}
        
        return results
    
    async def generate_response(self, query: str, intent: Dict[str, Any], 
                               results: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Generate natural language response based on query and results"""
        
        # For most queries, use the factual fallback response
        # Only use LLM for complex synthesis tasks
        query_lower = query.lower()
        
        # Use LLM only for summary/synthesis queries
        if "summary" in query_lower or "summarize" in query_lower:
            context_text = self._build_context_text(results, context)
            
            prompt = f"""Summarize the following video analysis in 2-3 sentences:

{context_text}

Summary (2-3 sentences only):"""

            try:
                response = self.llm(
                    prompt,
                    max_tokens=150,
                    temperature=0.5,
                    stop=["\n\n", "User:"],
                    echo=False
                )
                
                summary = response['choices'][0]['text'].strip()
                # Only take first paragraph to avoid rambling
                summary = summary.split('\n\n')[0]
                return summary
                
            except Exception as e:
                logger.error(f"Summary generation failed: {e}")
                return self._generate_fallback_response(query, results, context)
        
        # For all other queries, use factual fallback
        return self._generate_fallback_response(query, results, context)
    
    def _build_context_text(self, results: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Build context text from results and stored context"""
        parts = []
        
        if "transcription" in results:
            trans = results["transcription"]
            if "transcription" in trans and not trans.get("error"):
                text = trans['transcription'][:800]
                parts.append(f"Video transcription:\n{text}")
        
        if "vision" in results:
            vision = results["vision"]
            if "results" in vision and vision["results"]:
                frame_count = len(vision["results"])
                parts.append(f"\nVisual analysis: Analyzed {frame_count} frames from the video")
                # Add some details from first few frames
                for i, frame in enumerate(vision["results"][:2]):
                    if "caption" in frame:
                        parts.append(f"  Frame {i+1}: {frame['caption']}")
                    if "objects" in frame and frame["objects"]:
                        obj_list = ", ".join(frame["objects"][:5])
                        parts.append(f"  Objects detected: {obj_list}")
                
        if "pdf" in results:
            pdf = results["pdf"]
            if "output_path" in pdf:
                parts.append(f"\nPDF report generated: {pdf['output_path']}")
                
        if "pptx" in results:
            pptx = results["pptx"]
            if "output_path" in pptx:
                parts.append(f"\nPowerPoint generated: {pptx['output_path']}")
        
        if "summary" in results:
            parts.append(f"\nSummary: {results['summary']}")
        
        return "\n".join(parts) if parts else "No new information available"
    
    def _generate_fallback_response(self, query: str, results: Dict[str, Any], 
                                   context: Dict[str, Any]) -> str:
        """Generate a simple response when LLM fails"""
        
        if "error" in str(results):
            return "I encountered an issue processing your request. Please try again or rephrase your query."
        
        response_parts = []
        
        if "transcription" in results:
            trans = results["transcription"]
            if "transcription" in trans and not trans.get("error"):
                text = trans['transcription'][:500]
                if len(trans['transcription']) > 500:
                    text += "..."
                response_parts.append(f"Transcription:\n{text}")
            else:
                response_parts.append("Transcription completed.")
            
        if "vision" in results:
            vision = results["vision"]
            if "results" in vision and vision["results"]:
                frame_count = len(vision["results"])
                response_parts.append(f"\nAnalyzed {frame_count} frames from the video.")
                
                # Extract and list unique objects detected
                all_objects = set()
                captions = []
                
                for frame in vision["results"]:
                    if "objects" in frame and frame["objects"]:
                        for obj in frame["objects"]:
                            all_objects.add(obj.get("class", "unknown"))
                    
                    if "caption" in frame and len(captions) < 2:
                        captions.append(frame["caption"])
                
                if all_objects:
                    obj_list = ", ".join(sorted(all_objects)[:10])
                    response_parts.append(f"\nObjects detected: {obj_list}")
                
                if captions:
                    response_parts.append(f"\nScene descriptions:")
                    for i, cap in enumerate(captions, 1):
                        response_parts.append(f"  {i}. {cap}")
            else:
                response_parts.append("Visual analysis completed.")
            
        if "pdf" in results:
            pdf = results["pdf"]
            if "output_path" in pdf:
                response_parts.append(f"\nGenerated PDF report: {pdf['output_path']}")
                
        if "pptx" in results:
            pptx = results["pptx"]
            if "output_path" in pptx:
                response_parts.append(f"\nCreated PowerPoint: {pptx['output_path']}")
        
        return "\n".join(response_parts) if response_parts else "Task completed."
    
    async def generate_summary(self, context: Dict[str, Any]) -> str:
        """Generate summary of analysis results"""
        
        summary_parts = []
        
        if "transcription" in context:
            trans = context["transcription"]
            if "transcription" in trans:
                summary_parts.append(f"Audio content: {trans['transcription'][:300]}")
        
        if "vision_results" in context:
            vision = context["vision_results"]
            if "results" in vision:
                frames = vision["results"]
                summary_parts.append(f"Video analysis: Analyzed {len(frames)} frames")
        
        summary_text = "\n".join(summary_parts)
        
        prompt = f"""Provide a concise summary of this video analysis:

{summary_text}

Summary (2-3 sentences):"""

        try:
            response = self.llm(
                prompt,
                max_tokens=150,
                temperature=0.5,
                stop=["\n\n"],
                echo=False
            )
            
            return response['choices'][0]['text'].strip()
            
        except Exception as e:
            logger.warning(f"Summary generation failed: {e}")
            return "Analysis complete. Transcription and visual analysis available."
