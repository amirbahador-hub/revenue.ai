from django.urls import path, re_path
from .views import (
    TestCore,
    FileUploadView
)

app_name = "core"
urlpatterns = [
    path("", TestCore.as_view(), name="test"),
    re_path(r'^upload/(?P<filename>[^/]+)$', FileUploadView.as_view()),
]
