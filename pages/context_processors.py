"""Context processors for site-wide template variables."""

import json
from pathlib import Path

from django.conf import settings


DEFAULT_SITE = {
    "nav": [
        {"label": "首页", "href": "/"},
        {"label": "产品与方案", "href": "/products/"},
        {"label": "解决方案", "href": "/solutions/"},
        {"label": "案例", "href": "/cases/"},
        {"label": "联系我们", "href": "/contact/"},
    ],
    "cta": {"label": "预约演示", "href": "/contact/#demo"},
    "footer": {"brand": "小书仔阅读研究中心", "hotline": "400-960-7985"},
}


def site_config(request):
    """Load site.json and inject into every template as {{ site }}."""
    path = Path(settings.BASE_DIR) / "data" / "site.json"
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            data = DEFAULT_SITE
        # Merge with default so missing keys don't break templates
        nav = data.get("nav", DEFAULT_SITE["nav"])
        cta = data.get("cta", DEFAULT_SITE["cta"])
        footer = data.get("footer", DEFAULT_SITE["footer"])
        if not isinstance(nav, list):
            nav = DEFAULT_SITE["nav"]
        if not isinstance(cta, dict):
            cta = DEFAULT_SITE["cta"]
        if not isinstance(footer, dict):
            footer = DEFAULT_SITE["footer"]
        return {"site": {"nav": nav, "cta": cta, "footer": footer}}
    except Exception as e:
        print(f"[site_config] data/site.json load failed: {e}")
        return {"site": DEFAULT_SITE}
