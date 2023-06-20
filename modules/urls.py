from django.urls import path

from .views import ModuleListApi, ModuleDetailApi

app_name = "modules"

urlpatterns = [
    path("modules/", ModuleListApi.as_view(), name='module-list'),
    path("modules/<int:pk>/", ModuleDetailApi.as_view(), name='module-details')

]