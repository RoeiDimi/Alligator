from web_crawler import crawl
from web_page_data_handlers import handle_data

# Israeli Financial Sites
ISRAELI_FINANCE_SITES = [
    "https://www.globes.co.il/",
    "https://www.calcalist.co.il/",
    "https://www.themarker.com/",
    "https://www.bizportal.co.il/"
]
MAX_DEPTH = 1  # Shallow crawl just for headlines

if __name__ == '__main__':
    print(f"Starting crawl for Israeli Financial sites: {ISRAELI_FINANCE_SITES}")

    # Using the existing crawl module
    forrest = crawl.crawl(ISRAELI_FINANCE_SITES, MAX_DEPTH)

    # In a real application, we would parse the specific headlines here.
    # For now, we reuse the existing handle_data to store/process.
    handle_data.handle(filter(lambda tree: tree is not None, forrest))

    print("Israeli financial crawl finished.")
