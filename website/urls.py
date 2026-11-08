from django.urls import path
from .security_lab import (
    reflected_xss, sql_injection, insecure_invoice, open_redirect, exposed_config,
)
from .views import (
    HomePageView,
    AboutPageView,
    ContactPageView,
    BlogListView,
    BlogDetailView,
    BlogCreateView,
    BlogUpdateView,
    BlogDeleteView,
    BlogSearchView,
    EmailSuccess,
    BlogPostListAPIView,
    BlogPostDetailAPIView,
)

urlpatterns = [
    path("security-lab/xss/", reflected_xss, name="security_lab_xss"),
    path("security-lab/sqli/", sql_injection, name="security_lab_sqli"),
    path("security-lab/invoices/<int:invoice_id>/", insecure_invoice, name="security_lab_idor"),
    path("security-lab/redirect/", open_redirect, name="security_lab_redirect"),
    path("security-lab/config/", exposed_config, name="security_lab_config"),
    path("", HomePageView.as_view(), name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("contact/", ContactPageView.as_view(), name="contact"),
    path("contact/success/", EmailSuccess.as_view(), name="email_success"),
    path("blog/", BlogListView.as_view(), name="blog_posts"),
    path("blog/post/<uuid:pk>/", BlogDetailView.as_view(), name="blog_article"),
    path("blog/post/create/", BlogCreateView.as_view(), name="blog_article_create"),
    path(
        "blog/post/<uuid:pk>/update/",
        BlogUpdateView.as_view(),
        name="blog_article_update",
    ),
    path(
        "blog/post/<uuid:pk>/delete/",
        BlogDeleteView.as_view(),
        name="blog_article_delete",
    ),
    path("blog/search/", BlogSearchView.as_view(), name="blog_posts_search"),
    path("blog-api/v1/", BlogPostListAPIView.as_view(), name="blog_list_api"),
    path(
        "blog-api/v1/<uuid:pk>/",
        BlogPostDetailAPIView.as_view(),
        name="blog_detail_api",
    ),
]
