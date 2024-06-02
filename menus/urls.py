from django.urls import path
from .views import ModuleListApi, ModuleDetailApi

app_name = "menus"

urlpatterns = [
    path("modules/", ModuleListApi.as_view(), name="module-list"),
    path("modules/<int:pk>/", ModuleDetailApi.as_view(), name="module-detail"),
]