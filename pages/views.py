import json
import os
from pathlib import Path

from django.conf import settings
from django.http import Http404, HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect, render
from django.templatetags.static import static
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.http import FileResponse

from .forms import DemoRequestForm, SchemeRequestForm, DownloadLeadForm
from .models import DownloadLead


DEFAULT_HOME_SECTIONS = {
    "cache_ver": "20260216_01",
    "sections": {
        "products": {
            "title": "产品矩阵",
            "items": [
                {
                    "title": "漂流柜",
                    "desc": "图书漂流智能管理，轻松流转",
                    "poster": "posters/p1.jpg",
                    "href": "#",
                },
                {
                    "title": "自助借阅",
                    "desc": "一站式自助借还，高效便捷",
                    "poster": "posters/p2.jpg",
                    "href": "#",
                },
                {
                    "title": "电子绘本（微信端）",
                    "desc": "家长端随时随地阅读",
                    "poster": "posters/p3.jpg",
                    "href": "#",
                },
            ],
        },
        "solutions": {
            "title": "解决方案",
            "items": [
                {
                    "title": "园长",
                    "desc": "打造园所阅读特色，提升品牌影响力",
                    "poster": "posters/s1.jpg",
                    "href": "#",
                },
                {
                    "title": "教研员",
                    "desc": "丰富教学资源，助力课程建设",
                    "poster": "posters/s2.jpg",
                    "href": "#",
                },
                {
                    "title": "代理商",
                    "desc": "优质产品+完善服务，拓展区域市场",
                    "poster": "posters/s3.jpg",
                    "href": "#",
                },
            ],
        },
        "cases": {
            "title": "案例",
            "items": [
                {
                    "title": "案例一",
                    "desc": "占位文案",
                    "poster": "posters/c1.jpg",
                    "href": "#",
                },
                {
                    "title": "案例二",
                    "desc": "占位文案",
                    "poster": "posters/c2.jpg",
                    "href": "#",
                },
                {
                    "title": "案例三",
                    "desc": "占位文案",
                    "poster": "posters/c3.jpg",
                    "href": "#",
                },
            ],
        },
    },
}


def load_json(rel_path: str, default: dict):
    """Load JSON from data dir. Returns dict with cache_ver support. On error returns default and prints hint."""
    path = Path(settings.BASE_DIR) / rel_path
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"[load_json] {rel_path} load failed: {e}")
        return default


def load_hero_config():
    path = Path(settings.BASE_DIR) / "data" / "hero_videos.json"
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("videos", []), data.get("cache_ver", "20260216_01")


def load_home_sections():
    path = Path(settings.BASE_DIR) / "data" / "home_sections.json"
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return DEFAULT_HOME_SECTIONS
    cache_ver = data.get("cache_ver", "20260216_01")
    sections = data.get("sections", {})
    result = {"cache_ver": cache_ver, "sections": {}}
    for key in ("products", "solutions", "cases"):
        sec = sections.get(key, {}) if isinstance(sections, dict) else {}
        if not isinstance(sec, dict):
            sec = {}
        result["sections"][key] = {
            "title": sec.get("title", DEFAULT_HOME_SECTIONS["sections"][key]["title"]),
            "items": (
                sec.get("items", DEFAULT_HOME_SECTIONS["sections"][key]["items"])
                if isinstance(sec.get("items"), list)
                else DEFAULT_HOME_SECTIONS["sections"][key]["items"]
            ),
        }
    return result


DEFAULT_PRODUCTS = {
    "page_title": "产品与方案",
    "page_subtitle": "专业儿童阅读产品，助力园所打造智慧阅读环境",
    "items": [
        {
            "title": "漂流柜",
            "desc": "图书漂流智能管理，轻松流转",
            "poster": "posters/p1.jpg",
        },
        {
            "title": "自助借阅",
            "desc": "一站式自助借还，高效便捷",
            "poster": "posters/p1.jpg",
        },
        {
            "title": "电子绘本（微信端）",
            "desc": "家长端随时随地阅读",
            "poster": "posters/p1.jpg",
        },
    ],
    "cache_ver": "",
}

DEFAULT_SOLUTIONS = {
    "page_title": "解决方案",
    "page_subtitle": "针对不同角色的专业化解决方案",
    "items": [
        {
            "title": "园长",
            "desc": "打造园所阅读特色，提升品牌影响力",
            "poster": "posters/p1.jpg",
        },
        {
            "title": "教研员",
            "desc": "丰富教学资源，助力课程建设",
            "poster": "posters/p1.jpg",
        },
        {
            "title": "代理商",
            "desc": "优质产品+完善服务，拓展区域市场",
            "poster": "posters/p1.jpg",
        },
    ],
    "cache_ver": "",
}

DEFAULT_CASES = {
    "page_title": "案例",
    "page_subtitle": "看看我们的合作伙伴如何用阅读赋能教育",
    "items": [
        {"title": "案例一", "desc": "占位文案", "poster": "posters/p1.jpg"},
        {"title": "案例二", "desc": "占位文案", "poster": "posters/p1.jpg"},
        {"title": "案例三", "desc": "占位文案", "poster": "posters/p1.jpg"},
    ],
    "cache_ver": "",
}


def home(request):
    hero_videos, cache_ver = load_hero_config()
    home_cfg = load_home_sections()
    return render(
        request,
        "home.html",
        {
            "hero_videos": hero_videos,
            "CACHE_VER": cache_ver,
            "HOME_CFG": home_cfg,
        },
    )


def _poster_url(poster, cache_ver_qs):
    """Resolve poster to URL for template. Handles 'posters/x.jpg' or '/static/posters/x.jpg'."""
    if not poster:
        return ""
    poster = str(poster).strip()
    if poster.startswith(("http://", "https://", "/")):
        return poster + cache_ver_qs
    return static(poster) + cache_ver_qs


def _context_from_json(data, default, items_key="items"):
    """Build template context from JSON data. items_key: 'products' or 'items'."""
    if not data or not isinstance(data, dict):
        data = default
    items = data.get(items_key, data.get("items", default.get("items", [])))
    if not isinstance(items, list):
        items = default.get("items", [])
    page_title = data.get(
        "title", data.get("page_title", default.get("page_title", ""))
    )
    page_subtitle = data.get(
        "subtitle", data.get("page_subtitle", default.get("page_subtitle", ""))
    )
    cache_ver = data.get("cache_ver", default.get("cache_ver", ""))
    cache_ver_qs = "?v=" + cache_ver if cache_ver else ""
    for item in items:
        if isinstance(item, dict):
            poster = item.get("poster", item.get("image", ""))
            item["poster_url"] = _poster_url(poster, cache_ver_qs)
    return {
        "page_title": page_title,
        "page_subtitle": page_subtitle,
        "items": items,
        "cache_ver": cache_ver,
        "cache_ver_qs": cache_ver_qs,
    }


def products(request):
    data = load_json("data/products.json", DEFAULT_PRODUCTS)
    ctx = _context_from_json(data, DEFAULT_PRODUCTS, items_key="products")
    return render(request, "products.html", ctx)


def product_detail(request, pid):
    data = load_json("data/products.json", {"products": []})
    products_list = data.get("products", [])
    if not isinstance(products_list, list):
        products_list = []
    product = next(
        (
            p
            for p in products_list
            if isinstance(p, dict) and str(p.get("id")) == str(pid)
        ),
        None,
    )
    if product is None:
        raise Http404("Product not found")
    poster = product.get("poster", product.get("image", ""))
    cache_ver = data.get("cache_ver", "")
    cache_ver_qs = "?v=" + cache_ver if cache_ver else ""
    product = dict(product)
    product["poster_url"] = _poster_url(poster, cache_ver_qs)
    return render(request, "pages/product_detail.html", {"product": product})


def solutions(request):
    data = load_json("data/solutions.json", DEFAULT_SOLUTIONS)
    ctx = _context_from_json(data, DEFAULT_SOLUTIONS)
    return render(request, "solutions.html", ctx)


def cases(request):
    data = load_json("data/cases.json", DEFAULT_CASES)
    ctx = _context_from_json(data, DEFAULT_CASES)
    return render(request, "cases.html", ctx)


def case_detail(request, cid):
    data = load_json("data/cases.json", {"items": []})
    items = data.get("items", [])
    if not isinstance(items, list):
        items = []
    case = next(
        (c for c in items if isinstance(c, dict) and str(c.get("id")) == str(cid)),
        None,
    )
    if case is None:
        raise Http404("Case not found")
    poster = case.get("poster", case.get("image", ""))
    cache_ver = data.get("cache_ver", "")
    cache_ver_qs = "?v=" + cache_ver if cache_ver else ""
    case = dict(case)
    case["poster_url"] = _poster_url(poster, cache_ver_qs)
    content = case.get("content")
    case["content_is_list"] = isinstance(content, list)
    return render(request, "pages/case_detail.html", {"case": case})


def contact(request):
    demo_form = DemoRequestForm()
    scheme_form = SchemeRequestForm()

    if request.method == "POST":
        form_type = request.POST.get("form_type", "")

        if form_type == "demo":
            if request.POST.get("website"):
                return HttpResponseBadRequest()
            demo_form = DemoRequestForm(request.POST)
            if demo_form.is_valid():
                demo_form.save()
                return redirect(reverse("contact") + "?success=1#success")
        elif form_type == "scheme":
            if request.POST.get("website"):
                return HttpResponseBadRequest()
            scheme_form = SchemeRequestForm(request.POST)
            if scheme_form.is_valid():
                scheme_form.save()
                return redirect(reverse("contact") + "?success_scheme=1#plan")

    success = request.GET.get("success") == "1"
    success_scheme = request.GET.get("success_scheme") == "1"
    return render(
        request,
        "contact.html",
        {
            "form": demo_form,
            "scheme_form": scheme_form,
            "success": success,
            "success_scheme": success_scheme,
        },
    )


def resources(request):
    data = load_json(
        "data/resources.json", {"title": "资料下载", "subtitle": "", "products": []}
    )
    products = data.get("products", [])
    if not isinstance(products, list):
        products = []

    # 展平所有文件，按 file.id 建 file_map；无 id 的条目用索引补 id
    file_map = {}
    for item in products:
        for f in item.get("brochures") or []:
            f = dict(f)
            f["id"] = str(
                f.get("id")
                or ("brochure-%s-%s" % (item.get("product", ""), f.get("name", "")))
            )
            file_map[f["id"]] = f
        for f in item.get("specs") or []:
            f = dict(f)
            f["id"] = str(
                f.get("id")
                or ("spec-%s-%s" % (item.get("product", ""), f.get("name", "")))
            )
            file_map[f["id"]] = f

    all_files = list(file_map.values())
    # first_file = all_files[0] if all_files else None
    # req_id = (request.GET.get("id") or "").strip()
    # active_file = file_map.get(req_id) if req_id else first_file
    # if active_file is None and first_file:
    #     active_file = first_file

    req_id = (request.GET.get("id") or "").strip()
    active_file = file_map.get(req_id) if req_id else None

    return render(
        request,
        "pages/resources.html",
        {
            "page_title": data.get("title", "资料下载"),
            "page_subtitle": data.get("subtitle", ""),
            "products": products,
            "file_map": file_map,
            "active_file": active_file,
        },
    )


def _get_client_ip(request):
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "")


def _resolve_static_file(file_path_str: str):
    """解析并验证 /static/files/ 下的文件路径，返回 Path 或 None。"""
    file_path_str = (file_path_str or "").strip()
    prefix = "/static/files/"
    if not file_path_str.startswith(prefix):
        return None
    rel = file_path_str[len(prefix) :].lstrip("/")
    if ".." in rel or rel.startswith("/"):
        return None
    static_dir = Path(settings.BASE_DIR) / "static"
    full_path = (static_dir / "files" / rel).resolve()
    static_files_dir = (static_dir / "files").resolve()
    if not str(full_path).startswith(str(static_files_dir)) or not full_path.is_file():
        return None
    return full_path


@require_http_methods(["GET", "POST"])
def download(request):
    # GET: /download/?file=/static/files/xxx.pdf -> 直接返回文件
    if request.method == "GET":
        file_path_str = request.GET.get("file") or ""
        full_path = _resolve_static_file(file_path_str)
        if full_path is None:
            raise Http404("文件不存在")
        filename = os.path.basename(full_path)
        return FileResponse(
            open(full_path, "rb"), as_attachment=True, filename=filename
        )

    # POST: 表单登记后下载
    form = DownloadLeadForm(request.POST)
    if not form.is_valid():
        return JsonResponse({"ok": False, "errors": form.errors}, status=400)

    file_path = (request.POST.get("file_path") or "").strip()
    product_name = (request.POST.get("product_name") or "").strip()
    file_name = (request.POST.get("file_name") or "").strip()
    file_type = (request.POST.get("file_type") or "").strip()

    if not file_path or not product_name or not file_name:
        return JsonResponse(
            {"ok": False, "errors": {"__all__": ["缺少文件信息"]}}, status=400
        )

    full_path = _resolve_static_file(file_path)
    if full_path is None:
        return JsonResponse(
            {"ok": False, "errors": {"__all__": ["文件不存在或路径无效"]}}, status=404
        )

    cd = form.cleaned_data
    DownloadLead.objects.create(
        name=cd["name"],
        phone=cd["phone"],
        kindergarten=cd["kindergarten"],
        city=cd["city"],
        product_name=product_name,
        file_name=file_name,
        file_type=file_type,
        file_path=file_path,
        ip_address=_get_client_ip(request) or None,
        user_agent=request.META.get("HTTP_USER_AGENT", "")[:500],
    )

    filename_for_header = os.path.basename(full_path)
    response = FileResponse(
        open(full_path, "rb"), as_attachment=True, filename=filename_for_header
    )
    return response
