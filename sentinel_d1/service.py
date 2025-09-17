import asyncio
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn

from .manager import DownloadManager

app = FastAPI()
manager = DownloadManager()

@app.post("/add")
async def add_download(url: str, filename: str | None = None):
    job_id = await manager.add(url, filename)
    return {"job_id": job_id}

@app.get("/jobs")
def list_jobs():
    return {"jobs": [job.as_dict() for job in manager.jobs.values()]}

@app.post("/pause/{job_id}")
def pause(job_id: int):
    manager.pause(job_id)
    return JSONResponse({"paused": job_id})

@app.post("/resume/{job_id}")
async def resume(job_id: int):
    await manager.resume(job_id)
    return {"resumed": job_id}

@app.delete("/remove/{job_id}")
def remove(job_id: int):
    manager.remove(job_id)
    return {"removed": job_id}

def run_service(host="127.0.0.1", port=8765):
    uvicorn.run(app, host=host, port=port)
