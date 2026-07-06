import asyncio
import logging
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import aiohttp

from config import settings
from storage import storage

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

app = FastAPI()

templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)


async def check_single_proxy(session: aiohttp.ClientSession, proxy_url: str) -> dict:
    """Asynchronously checks a single proxy and logs the result."""
    start_time = asyncio.get_event_loop().time()
    try:
        async with session.get(settings.TEST_URL, proxy=proxy_url, timeout=settings.TIMEOUT_SECONDS) as response:
            if response.status == 200:
                latency_ms = (asyncio.get_event_loop().time() - start_time) * 1000
                status = "fast" if latency_ms <= settings.FAST_THRESHOLD_MS else "slow"

                logger.info(f"Proxy {proxy_url} is {status.upper()} (Latency: {int(latency_ms)}ms)")
                return {"url": proxy_url, "status": status, "latency": f"{int(latency_ms)} ms"}
    except Exception as e:
        logger.warning(f"Proxy {proxy_url} failed. Error: {e}")

    return {"url": proxy_url, "status": "dead", "latency": "N/A"}


@app.get("/", response_class=HTMLResponse)
async def get_index_page(request: Request):
    """Renders the main dashboard page with the initial unchecked proxy list."""
    logger.info("Index page requested. Returning proxy list without checking.")
    proxy_list = [{"url": p, "status": "not_checked", "latency": "—"} for p in storage.proxies]
    return templates.TemplateResponse(request=request, name="index.html", context={"proxies": proxy_list})


@app.get("/check", response_class=HTMLResponse)
async def check_all_proxies(request: Request):
    """Triggers the asynchronous mass checking of all proxies and updates the UI."""
    logger.info(f"Starting async check for {len(storage.proxies)} proxies...")

    async with aiohttp.ClientSession() as session:
        tasks = [check_single_proxy(session, proxy) for proxy in storage.proxies]
        results = await asyncio.gather(*tasks)

    logger.info("All proxies checked successfully.")
    return templates.TemplateResponse(request=request, name="index.html", context={"proxies": results})


@app.post("/add")
async def add_new_proxy(proxy_url: str = Form(...)):
    """Adds a new proxy to the in-memory storage."""
    if proxy_url and proxy_url not in storage.proxies:
        storage.proxies.append(proxy_url)
        logger.info(f"New proxy added: {proxy_url}. Total count: {len(storage.proxies)}")
    return RedirectResponse(url="/", status_code=303)


@app.post("/delete")
async def delete_existing_proxy(proxy_url: str = Form(...)):
    """Removes a proxy from the in-memory storage."""
    if proxy_url in storage.proxies:
        storage.proxies.remove(proxy_url)
        logger.info(f"Proxy removed: {proxy_url}. Total count: {len(storage.proxies)}")
    return RedirectResponse(url="/", status_code=303)
