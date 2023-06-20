from rest_framework.views import APIView
from rest_framework import serializers, status
from rest_framework.response import Response
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from modules.models import Module

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ('id', 'name')

class ModuleListApi(APIView):

    def get(self, request):
        modules = Module.objects.all()
        serializer = ModuleSerializer(modules, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            serializer = ModuleSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            new_module = Module.objects.execute_create(
                        **serializer.validated_data)
            output_serializer = ModuleSerializer(new_module)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(e.message_dict, status=status.HTTP_400_BAD_REQUEST)
        
class ModuleDetailApi(APIView):
    def get(self, request, pk):
        try:
            module = Module.objects.find_by_pk(pk)
            output_serializer = ModuleSerializer(module)
            return Response(output_serializer.data, status=status.HTTP_200_OK)
        except ValidationError as  err:
            return Response(err, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            serializer = ModuleSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            update_module = Module.objects.execute_update(
                    pk, **serializer.validated_data)
            output_serializer = ModuleSerializer(update_module)
            return Response(output_serializer.data, status=status.HTTP_200_OK)
        
        except ValidationError as e:
            return Response(e.message_dict, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        try:
            Module.objects.execute_delete(pk=pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist as err:
            return Response(status=status.HTTP_404_NOT_FOUND)