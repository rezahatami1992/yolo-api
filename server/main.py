from fastapi import FastAPI, File, UploadFile, HTTPException
from ultralytics import YOLO
import uvicorn
from PIL import Image
import io

# Initialize FastAPI app
app = FastAPI(title="YOLO Object Detection API")

# Load YOLO model (will download automatically on first run)
model = YOLO('yolov8n.pt')  # nano version for speed

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "YOLO API is running!", "model": "YOLOv8n"}

@app.post("/detect")
async def detect_objects(file: UploadFile = File(...)):
    """
    Detect objects in uploaded image
    """
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read and process image
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))
        
        # Run YOLO detection
        results = model(image)
        
        # Extract detection results
        detections = []
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    detection = {
                        "class_name": model.names[int(box.cls[0])],
                        "confidence": float(box.conf[0]),
                        "bbox": box.xyxy[0].tolist()  # [x1, y1, x2, y2]
                    }
                    detections.append(detection)
        
        return {
            "filename": file.filename,
            "detections": detections,
            "total_objects": len(detections)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Detection failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 
