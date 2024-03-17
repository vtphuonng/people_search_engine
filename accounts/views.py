from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import BasicInformation, ContactInfo
from .serializers import BasicInformationSerializer, ContactInfoSerializer

class BasicInformationList(APIView):
    """
    View to list all basic information records.
    """
    def get(self, request):
        basic_info = BasicInformation.objects.all()
        serializer = BasicInformationSerializer(basic_info, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BasicInformationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BasicInformationDetail(APIView):
    """
    View to retrieve, update or delete a basic information record.
    """
    def get_object(self, pk):
        try:
            return BasicInformation.objects.get(pk=pk)
        except BasicInformation.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        basic_info = self.get_object(pk)
        serializer = BasicInformationSerializer(basic_info)
        return Response(serializer.data)

    def put(self, request, pk):
        basic_info = self.get_object(pk)
        serializer = BasicInformationSerializer(basic_info, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        basic_info = self.get_object(pk)
        basic_info.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContactInfoList(APIView):
    """
    View to list all contact information records.
    """
    def get(self, request):
        contact_info = ContactInfo.objects.all()
        serializer = ContactInfoSerializer(contact_info, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ContactInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContactInfoDetail(APIView):
    """
    View to retrieve, update or delete a contact information record.
    """
    def get_object(self, pk):
        try:
            return ContactInfo.objects.get(pk=pk)
        except ContactInfo.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        contact_info = self.get_object(pk)
        serializer = ContactInfoSerializer(contact_info)
        return Response(serializer.data)

    def put(self, request, pk):
        contact_info = self.get_object(pk)
        serializer = ContactInfoSerializer(contact_info, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        contact_info = self.get_object(pk)
        contact_info.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
