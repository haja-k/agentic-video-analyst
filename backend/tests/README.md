# Test Scripts

This directory contains test scripts for all AI agents in the video analysis system.

## Test Scripts

### test_transcription.py
Test the TranscriptionAgent with Whisper speech-to-text.

```bash
cd backend/tests
source ../venv/bin/activate
python test_transcription.py ../uploads/your_video.mp4
```

**Output:** `results/transcription_result.json`

### test_vision.py
Test the VisionAgent with BLIP-2 image captioning and YOLOv8 object detection.

```bash
cd backend/tests
source ../venv/bin/activate
python test_vision.py ../uploads/your_video.mp4
```

**Output:** `results/vision_result.json`

### test_generation.py
Test the GenerationAgent to create PDF and PowerPoint reports from previous results.

```bash
cd backend/tests
source ../venv/bin/activate
python test_generation.py
```

**Outputs:**
- `results/video_report.pdf`
- `results/video_presentation.pptx`

### test_models.py
Verify all AI models and dependencies are correctly installed.

```bash
cd backend/tests
source ../venv/bin/activate
python test_models.py
```

## Results Directory

All test outputs are saved in `results/`:
- `transcription_result.json` - Full transcription with timestamps
- `vision_result.json` - Frame analysis with objects and captions
- `video_report.pdf` - Comprehensive PDF report
- `video_presentation.pptx` - PowerPoint presentation

## Running Tests

Always activate the virtual environment first:

```bash
cd backend
source venv/bin/activate
cd tests
```

Then run the desired test script.
