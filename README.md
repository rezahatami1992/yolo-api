# YOLO Object Detection API

A FastAPI-based object detection service using YOLOv8 from Ultralytics.

## Features

- RESTful API for object detection
- Supports common image formats (JPG, PNG, etc.)
- Returns detected objects with bounding boxes and confidence scores
- Easy to use client for testing

## Project Structure

```
yolo-api/
├── server/
│   ├── main.py           # FastAPI server
│   └── requirements.txt  # Server dependencies
├── client/
│   ├── test_client.py    # Test client
│   └── requirements.txt  # Client dependencies
└── models/               # YOLO models (auto-downloaded)
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/rezahatami1992/yolo-api
cd yolo-api
```

2. Create virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
```

3. Install server dependencies:
```bash
cd server
pip install -r requirements.txt
```

4. Install client dependencies:
```bash
cd ../client
pip install -r requirements.txt
```

## Usage

### Start the Server
```bash
cd server
python main.py
```
Server will run on `http://localhost:8000`

### Test with Client
```bash
cd client
python test_client.py
```
Follow the prompts to upload an image for detection.

### API Endpoints

- `GET /` - Health check
- `POST /detect` - Upload image for object detection

## Response Format

```json
{
  "filename": "image.jpg",
  "detections": [
    {
      "class_name": "person",
      "confidence": 0.85,
      "bbox": [100, 150, 300, 400]
    }
  ],
  "total_objects": 1
}
```

## Requirements

- Python 3.8+
- FastAPI
- Ultralytics YOLOv8
- PIL/Pillow

## License

MIT License
