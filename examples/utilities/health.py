from dotenv import load_dotenv
load_dotenv()

from scrapegraph_py import ScrapeGraphAI

sgai = ScrapeGraphAI()

res = sgai.health()

if res.status == "success":
    print("Status:", res.data.status)
    print("Uptime:", res.data.uptime, "seconds")
    if res.data.services:
        print("Services:")
        print("  Redis:", res.data.services.redis)
        print("  DB:", res.data.services.db)
else:
    print("Failed:", res.error)
