from __future__ import annotations

import os
import platform
from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("scrapegraph-py")
except PackageNotFoundError:  # local checkout without an installed distribution
    __version__ = "unknown"

USER_AGENT = f"scrapegraph-py/{__version__} python/{platform.python_version()}"


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
        return os.environ.get("SGAI_API_URL") or "https://v2-api.scrapegraphai.com/api"


env = Env()
