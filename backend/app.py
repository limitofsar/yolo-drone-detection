from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil
import uuid
import threading
import queue
import cv2

from src.yolo_loader import get_model, available_models

app = FastAPI(title="YOLO Video Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

TASKS_DIR = Path("../tasks")
TASKS_DIR.mkdir(exist_ok=True)

task_queue = queue.Queue()
tasks_status = {}

VEHICLE_CLASSES = [2, 3, 4, 5, 6, 7, 8, 9]

def process_video_task(task_id, file_path, model_name, line_width):
    model = get_model(model_name)

    cap = cv2.VideoCapture(str(file_path))
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    output_path = TASKS_DIR / f"{task_id}.mp4"
    out = cv2.VideoWriter(
        str(output_path),
        cv2.VideoWriter_fourcc(*"avc1"),
        fps,
        (w, h),
    )

    tasks_status[task_id] = {"status": "processing", "progress": 0}

    for i in range(frames):
        ret, frame = cap.read()
        if not ret:
            break

        result = model.predict(frame, classes=VEHICLE_CLASSES, conf=0.5, iou=0.5)[0]

        annotated = result.plot(line_width=line_width)

        out.write(annotated)
        tasks_status[task_id]["progress"] = int((i + 1) / frames * 100)

    cap.release()
    out.release()

    tasks_status[task_id]["status"] = "done"
    tasks_status[task_id]["result"] = str(output_path)

def worker():
    while True:
        task = task_queue.get()
        process_video_task(**task)
        task_queue.task_done()

threading.Thread(target=worker, daemon=True).start()


@app.get("/models")
def models():
    return {
        "models": available_models()
    }

@app.post("/upload")
async def upload_video(
    file: UploadFile,
    model_name: str = Form("YOLOv8n"),
    line_width: int = Form(2),
):
    task_id = str(uuid.uuid4())
    task_dir = TASKS_DIR / task_id
    task_dir.mkdir()

    input_path = task_dir / file.filename
    with input_path.open("wb") as f:
        shutil.copyfileobj(file.file, f)

    tasks_status[task_id] = {"status": "queued", "progress": 0}

    task_queue.put({
        "task_id": task_id,
        "file_path": input_path,
        "model_name": model_name,
        "line_width": line_width,
    })

    return {"task_id": task_id}

@app.get("/status/{task_id}")
def status(task_id: str):
    return tasks_status.get(task_id, {"error": "not found"})

@app.get("/result/{task_id}")
def result(task_id: str):
    task = tasks_status.get(task_id)
    if not task or task["status"] != "done":
        return JSONResponse(status_code=400, content={"error": "not ready"})
    return FileResponse(task["result"], media_type="video/mp4")
