import requests
import json
import sys
import os

# Server configuration
SERVER_URL = "http://localhost:8000"
DETECT_ENDPOINT = f"{SERVER_URL}/detect"

def test_server_health():
    """Test if server is running"""
    try:
        response = requests.get(SERVER_URL)
        if response.status_code == 200:
            print("✓ Server is running!")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"✗ Server returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to server. Is it running?")
        return False

def detect_objects_in_image(image_path):
    """Send image to server for object detection"""
    
    # Check if file exists
    if not os.path.exists(image_path):
        print(f"✗ Image file not found: {image_path}")
        return None
    
    try:
        # Prepare file for upload
        with open(image_path, 'rb') as image_file:
            files = {'file': (os.path.basename(image_path), image_file, 'image/jpeg')}
            
            print(f"📤 Uploading image: {image_path}")
            response = requests.post(DETECT_ENDPOINT, files=files)
        
        if response.status_code == 200:
            result = response.json()
            print("✓ Detection successful!")
            print(f"📊 Results:")
            print(f"   - File: {result['filename']}")
            print(f"   - Total objects found: {result['total_objects']}")
            
            # Print each detection
            for i, detection in enumerate(result['detections'], 1):
                print(f"   {i}. {detection['class_name']} "
                      f"(confidence: {detection['confidence']:.2f})")
            
            return result
            
        else:
            print(f"✗ Detection failed with status code: {response.status_code}")
            print(f"Error: {response.text}")
            return None
            
    except Exception as e:
        print(f"✗ Error occurred: {str(e)}")
        return None

def main():
    """Main function"""
    print("=== YOLO API Test Client ===")
    
    # Test server health
    if not test_server_health():
        print("\n❌ Please start the server first!")
        print("Run: python server/main.py")
        return
    
    # Get image path from user
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        image_path = input("\n📁 Enter path to image file: ").strip()
    
    # Detect objects
    detect_objects_in_image(image_path)

if __name__ == "__main__":
    main()
