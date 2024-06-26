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

class ModuleMoveSerializer(serializers.Serializer):
    move = serializers.CharField(max_length=30)
    to = serializers.IntegerField()

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
    def get(self, request, pk):
        try:
            module_tree = Menu.objects.get_module_tree(pk)
            output_serializer = ModuleSerializer(module_tree, many=True)
            return Response(output_serializer.data, status=status.HTTP_200_OK)
        except ValidationError as  err:
            return Response(err, status=status.HTTP_404_NOT_FOUND)

class ModuleOperationApi(APIView):
    
    def put(self, request, pk_module):
        serializer = ModuleMoveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        move_type = data.get('move')
        pk_sibling = data.get('to')
       
        Menu.objects.move(node_origin_id=pk_module, move_type=move_type, node_sibling_id=pk_sibling ) 
        return Response({}, status=status.HTTP_200_OK)
    