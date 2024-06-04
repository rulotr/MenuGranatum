from django.urls import path
from .views import ModuleListApi, ModuleDetailApi, ModuleOperationApi

app_name = "menus"

urlpatterns = [
    path("modules/", ModuleListApi.as_view(), name="module-list"),
    path("modules/<int:pk>/", ModuleDetailApi.as_view(), name="module-detail"),
    path("modules/<int:pk_module>/move_before/<int:pk_sibling>", ModuleOperationApi.as_view(), name="module-move-before"),
]