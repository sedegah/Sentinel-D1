import asyncio
from rich.live import Live
from rich.table import Table
from .downloader import DownloadJob

class DownloadManager:
    def __init__(self):
        self.jobs = {}
        self.next_id = 1

    async def add(self, url, filename=None):
        job = DownloadJob(self.next_id, url, filename)
        self.jobs[self.next_id] = job
        self.next_id += 1
        asyncio.create_task(job.start())

    def pause(self, job_id):
        if job_id in self.jobs:
            self.jobs[job_id].pause()

    async def resume(self, job_id):
        if job_id in self.jobs:
            await self.jobs[job_id].resume()

    def remove(self, job_id):
        if job_id in self.jobs:
            self.jobs[job_id].cancel()
            del self.jobs[job_id]

    def list_table(self):
        return self._make_table()

    async def dashboard(self):
        with Live(auto_refresh=False) as live:
            while True:
                live.update(self._make_table(), refresh=True)
                await asyncio.sleep(0.5)

    def _make_table(self):
        t = Table(title="Sentinel-D1 Downloads")
        t.add_column("ID", justify="right")
        t.add_column("File")
        t.add_column("Status")
        t.add_column("Progress")
        t.add_column("Speed (KB/s)")
        for job in self.jobs.values():
            t.add_row(
                str(job.job_id),
                job.filename,
                job.status,
                f"{job.percent:.1f}%",
                f"{job.speed:.1f}",
            )
        return t
