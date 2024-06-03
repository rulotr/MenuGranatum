from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from django.core.exceptions import ValidationError

from menus.models import Menu

# Create your views here.
class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id', 'name', 'path', 'depth', 'order']

class ModulePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id', 'name']
        extra_kwargs = {'id': {'read_only': False, 'required': False}}


class ModuleListApi(APIView):
    def get(self, request):
        modules = Menu.objects.get_all_modules()
        serializer = ModuleSerializer(modules, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            serializer = ModulePostSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            menu_data = serializer.validated_data
            new_module = Menu.objects.execute_create(
                name=menu_data.get('name'), id=menu_data.get('id'))
             
            output_serializer = ModuleSerializer(new_module)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(e.message_dict, status=status.HTTP_400_BAD_REQUEST)


class ModuleDetailApi(APIView):
    pass