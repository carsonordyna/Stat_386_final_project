import asyncio
from datetime import timedelta
from crawlee.crawlers import PlaywrightCrawler, PlaywrightCrawlingContext
from crawlee import Request, ConcurrencySettings
import csv
import re
import psutil
import os

MAX_MEMORY_GB = 7.0
CSV_FILE = 'Salt_Lake_County_housing_data.csv'

CSV_HEADERS = [
    'mls', 'price', 'address', 'beds', 'baths', 'sqft',
    'year_built', 'lot_size', 'garage', 'agent', 'city'
]

visited_mls = set()


# ---------------- UTILITIES ----------------

def check_memory():
    process = psutil.Process(os.getpid())
    mem_gb = process.memory_info().rss / (1024 ** 3)
    if mem_gb > MAX_MEMORY_GB * 0.9:
        raise MemoryError(f"Approaching memory limit: {mem_gb:.2f}GB / {MAX_MEMORY_GB}GB")
    return mem_gb


def init_csv():
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
        writer.writeheader()


def append_to_csv(data: dict):
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
        writer.writerow({k: data.get(k, "") for k in CSV_HEADERS})


async def safe_text(page, selector):
    try:
        el = await page.query_selector(selector)
        if el:
            txt = await el.text_content()
            return (txt or "").strip()
    except:
        return ""
    return ""


def is_valid_url(url: str) -> bool:
    if not url:
        return False
    return not any(url.lower().startswith(p) for p in ("javascript:", "mailto:", "tel:", "#"))


# ---------------- MAIN ----------------

async def main():
    init_csv()

    cities = [
        "draper", "holladay", "midvale", "millcreek", "cottonwood-heights",
        "murray", "salt-lake-city", "sandy", "south-jordan", "south-salt-lake",
        "sugarhouse", "west-jordan","west-valley"
    ]

    start_urls = [
        f"https://www.utahrealestate.com/{c}-homes" for c in cities
    ]

    crawler = PlaywrightCrawler(
        headless=True,
        browser_type='firefox',
        max_request_retries=2,
        max_requests_per_crawl=2000,

        concurrency_settings=ConcurrencySettings(
            min_concurrency=2,
            max_concurrency=5,
            desired_concurrency=3,
        ),
        request_handler_timeout=timedelta(seconds=60),
    )

    @crawler.router.default_handler
    async def router_handler(context: PlaywrightCrawlingContext):
        url = context.request.url

        mem = check_memory()
        context.log.info(f"Memory OK: {mem:.2f}GB")

        await context.page.wait_for_load_state("domcontentloaded")
        await asyncio.sleep(1)

        if "/listing/" in url or context.request.label == "detail":
            await extract_detail(context)
        else:
            await extract_search_results(context)

    await crawler.run(start_urls)
    crawler.log.info(f"🎉 Done! Saved output → {CSV_FILE}")


# ---------------- SEARCH RESULTS ----------------

async def extract_search_results(context: PlaywrightCrawlingContext):
    page = context.page
    url = context.request.url

    # determine city from URL slug
    match = re.search(r"utahrealestate\.com/([^/]+)-homes", url)
    city = match.group(1) if match else "unknown"

    try:
        await page.wait_for_selector(".property___card", timeout=15000)
    except:
        context.log.warning("No listings found")
        return

    cards = await page.query_selector_all(".property___card")
    context.log.info(f"Found {len(cards)} listings for city {city}")

    for card in cards:
        try:
            mls = await card.get_attribute("listno")
            if not mls or mls in visited_mls:
                continue

            visited_mls.add(mls)
            detail_url = f"https://www.utahrealestate.com/listing/{mls}"

            await context.add_requests([
                Request.from_url(
                    detail_url,
                    label="detail",
                    user_data={"city": city}
                )
            ])

        except Exception as e:
            context.log.error(f"Error queuing listing: {e}")

    # pagination
    next_btn = await page.query_selector('a.next, a:has-text("Next"), a:has-text("»")')
    if next_btn:
        href = await next_btn.get_attribute("href")
        if href and is_valid_url(href):
            if href.startswith("/"):
                href = f"https://www.utahrealestate.com{href}"

            await context.add_requests([
                Request.from_url(href, user_data={"city": city})
            ])


# ---------------- DETAIL PAGE ----------------

async def extract_detail(context: PlaywrightCrawlingContext):
    page = context.page
    url = context.request.url

    # city passed from search page
    city = context.request.user_data.get("city", "unknown")

    mls = url.split("/listing/")[-1].split("/")[0]
    await asyncio.sleep(1)

    street = await safe_text(page, ".prop___overview h2")
    city_state = await safe_text(page, "#location-data")
    address = f"{street}, {city_state}".strip(" ,")

    price = await safe_text(page, ".prop-details-overview li span")

    beds = (await safe_text(page, ".prop-details-overview li:nth-of-type(2) span")).replace(",", "")
    baths = (await safe_text(page, ".prop-details-overview li:nth-of-type(3) span")).replace(",", "")
    sqft = (await safe_text(page, ".prop-details-overview li:nth-of-type(4) span")).replace(",", "")

    html = await page.content()

    year_built = ""
    lot_size = ""
    garage = ""

    if m := re.search(r"Year\s*Built[^0-9]*(\d{4})", html, re.I):
        year_built = m.group(1)

    if m := re.search(r"Lot[^0-9]*([\d.,]+\s*(?:ac|acre|sq\.? ft))", html, re.I):
        lot_size = m.group(1)

    if m := re.search(r"Garage[^0-9]*(\d+)", html, re.I):
        garage = m.group(1)

    agent = await safe_text(page, ".agent-name, [class*='agent']")
    agent = re.sub(r"\s+", " ", agent).strip() if agent else ""

    data = {
        "mls": mls,
        "price": price,
        "address": address,
        "beds": beds,
        "baths": baths,
        "sqft": sqft,
        "year_built": year_built,
        "lot_size": lot_size,
        "garage": garage,
        "agent": agent,
        "city": city
    }

    append_to_csv(data)
    context.log.info(f"✔ Saved MLS {mls} ({city}) | {price} | {beds}/{baths} | {sqft} sqft")


# ---------------- RUN ----------------

if __name__ == "__main__":
    asyncio.run(main())
