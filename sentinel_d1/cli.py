import typer, requests
from rich.console import Console
from rich.table import Table
from .service import run_service

app = typer.Typer(help="Sentinel-D1 CLI client")
BASE = "http://127.0.0.1:8765"

@app.command()
def serve(host: str = "127.0.0.1", port: int = 8765):
    """Start the Sentinel-D1 background service."""
    run_service(host, port)

@app.command()
def add(url: str, filename: str = None):
    r = requests.post(f"{BASE}/add", params={"url": url, "filename": filename})
    typer.echo(f"Queued job {r.json()['job_id']}")

@app.command()
def list():
    r = requests.get(f"{BASE}/jobs")
    jobs = r.json()["jobs"]
    t = Table(title="Sentinel-D1 Downloads")
    for col in ["ID","File","Status","Progress","Speed"]:
        t.add_column(col)
    for j in jobs:
        t.add_row(str(j["id"]), j["filename"], j["status"],
                  f"{j['percent']}%", f"{j['speed']} KB/s")
    Console().print(t)

@app.command()
def pause(job_id: int):
    requests.post(f"{BASE}/pause/{job_id}")
    typer.echo(f"Paused {job_id}")

@app.command()
def resume(job_id: int):
    requests.post(f"{BASE}/resume/{job_id}")
    typer.echo(f"Resumed {job_id}")

@app.command()
def remove(job_id: int):
    requests.delete(f"{BASE}/remove/{job_id}")
    typer.echo(f"Removed {job_id}")
