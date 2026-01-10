#!/usr/bin/env python3
"""Test query flow from HTTP bridge to gRPC server"""

import asyncio
import json
import requests

async def test_query():
    """Test a query with an existing video"""
    
    # First, check if we have any videos
    base_url = "http://localhost:8080"
    
    print("Testing query flow...")
    print("=" * 60)
    
    # Use one of the existing videos
    video_id = "693d1b6f-63cf-42a7-9319-fdf4e5e2a1cf"
    
    query_data = {
        "videoId": video_id,
        "query": "describe the scene in this video",
        "sessionId": "test_session_123"
    }
    
    print(f"\n1. Sending query to HTTP bridge...")
    print(f"   URL: {base_url}/query")
    print(f"   Data: {json.dumps(query_data, indent=2)}")
    
    try:
        response = requests.post(
            f"{base_url}/query",
            json=query_data,
            timeout=30
        )
        
        print(f"\n2. Response Status: {response.status_code}")
        
        if response.ok:
            result = response.json()
            print(f"\n3. Response received:")
            print(json.dumps(result, indent=2))
        else:
            print(f"\n3. Error response:")
            print(response.text)
            
    except Exception as e:
        print(f"\n3. Exception: {e}")

if __name__ == "__main__":
    asyncio.run(test_query())
