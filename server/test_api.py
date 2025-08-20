#!/usr/bin/env python3
"""
Simple test script to verify the FastAPI server is working correctly
"""

import requests
import json

def test_api():
    """Test the API endpoints"""
    base_url = "http://localhost:8001"
    
    print("🧪 Testing Startup Business Guide API...")
    print("=" * 50)
    
    try:
        # Test root endpoint
        print("📍 Testing root endpoint...")
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Root endpoint working!")
            print(f"   Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
        
        print()
        
        # Test health endpoint
        print("🏥 Testing health endpoint...")
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health endpoint working!")
            print(f"   Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
        
        print()
        
        # Test ask endpoint with sample question
        print("🤖 Testing ask endpoint...")
        test_question = {
            "question": "What documents do I need to travel from Kenya to Ireland?",
            "context": "I'm a Kenyan citizen planning to visit Ireland for business",
            "user_id": "test_user_123"
        }
        
        response = requests.post(
            f"{base_url}/api/ask",
            json=test_question,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print("✅ Ask endpoint working!")
            result = response.json()
            print(f"   Question: {test_question['question']}")
            print(f"   Answer: {result['answer'][:200]}...")
            print(f"   Confidence: {result['confidence']}")
            print(f"   Processing time: {result['processing_time']}s")
            print(f"   Model used: {result['model_used']}")
        else:
            print(f"❌ Ask endpoint failed: {response.status_code}")
            print(f"   Error: {response.text}")
        
        print()
        print("🎉 API testing complete!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to the server. Is it running on port 8001?")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_api()
