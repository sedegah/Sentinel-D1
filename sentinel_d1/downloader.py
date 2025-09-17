import aiohttp, asyncio, os, time

class DownloadJob:
    def __init__(self, job_id, url, filename=None):
        self.job_id = job_id
        self.url = url
        self.filename = filename or url.split("/")[-1]
        self.percent = 0.0
        self.speed = 0.0
        self.status = "Queued"
        self._pause_event = asyncio.Event()
        self._pause_event.set()
        self._stop = False

    async def start(self):
        self.status = "Downloading"
        while not self._stop:
            await self._pause_event.wait()
            try:
                await self._download()
                self.status = "Completed"
                break
            except Exception as e:
                self.status = f"Error: {e}"
                await asyncio.sleep(3)

    def pause(self):
        self.status = "Paused"
        self._pause_event.clear()

    async def resume(self):
        self.status = "Downloading"
        self._pause_event.set()

    def cancel(self):
        self.status = "Cancelled"
        self._stop = True

    async def _download(self):
        async with aiohttp.ClientSession() as s:
            async with s.head(self.url) as r:
                total = int(r.headers.get("Content-Length", 0))
            downloaded = os.path.getsize(self.filename) if os.path.exists(self.filename) else 0
            headers = {"Range": f"bytes={downloaded}-"}
            mode = "ab" if downloaded else "wb"
            start_time = time.time()

            async with s.get(self.url, headers=headers) as r:
                with open(self.filename, mode) as f:
                    async for chunk in r.content.iter_chunked(1024 * 64):
                        await self._pause_event.wait()
                        if self._stop:
                            break
                        f.write(chunk)
                        downloaded += len(chunk)
                        self.percent = downloaded * 100 / total
                        elapsed = time.time() - start_time
                        self.speed = downloaded / 1024 / elapsed if elapsed else 0




    def as_dict(self):
        return {
            "id": self.job_id,
            "filename": self.filename,
            "status": self.status,
            "percent": f"{self.percent:.2f}",
            "speed": f"{self.speed:.2f}"
        }
