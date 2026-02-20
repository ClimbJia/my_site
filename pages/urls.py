from django.urls import path
from .views import (
    home,
    products,
    product_detail,
    solutions,
    cases,
    case_detail,
    contact,
    resources,
    download,
)

urlpatterns = [
    path("", home, name="home"),
    path("products/", products, name="products"),
    path("products/<str:pid>/", product_detail, name="product_detail"),
    path("solutions/", solutions, name="solutions"),
    path("cases/", cases, name="cases"),
    path("cases/<str:cid>/", case_detail, name="case_detail"),
    path("contact/", contact, name="contact"),
    path("resources/", resources, name="resources"),
    path("download/", download, name="download"),
]
