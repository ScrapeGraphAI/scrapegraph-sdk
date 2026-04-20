from __future__ import annotations

import os


class Env:
    @property
    def debug(self) -> bool:
        return os.environ.get("SGAI_DEBUG") == "1"

    @property
    def timeout(self) -> int:
        val = os.environ.get("SGAI_TIMEOUT")
        return int(val) if val else 120

    @property
    def base_url(self) -> str:
        return os.environ.get("SGAI_API_URL") or "https://v2-api.scrapegraphai.com/api/v2"


env = Env()
