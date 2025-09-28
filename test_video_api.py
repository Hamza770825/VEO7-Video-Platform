import requests
import json

def test_video_generation():
    url = "http://localhost:8000/api/generate-video"
    
    # Read the test image
    with open("test_image.svg", "rb") as f:
        image_data = f.read()
    
    # Prepare form data
    files = {
        'image': ('test_image.svg', image_data, 'image/svg+xml')
    }
    
    data = {
        'text': 'Hello World from VEO7',
        'language': 'en',
        'voice_speed': '1.0',
        'user_id': 'demo-user-123'
    }
    
    try:
        print("Sending request to generate video...")
        response = requests.post(url, files=files, data=data, timeout=120)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("Success!")
            print(json.dumps(result, indent=2))
        else:
            print(f"Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    test_video_generation()