from asyncio.log import logger
import logging
from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from to_do.models import Entry
from to_do.serializers import ToDoSerializer
from rest_framework.decorators import api_view

from getTimeStamp import getStamp

# Create your views here.

@api_view(['GET'])
def list_to_do(request):
    entries = Entry.objects.all()
    entries_serializers = ToDoSerializer(entries, many = True)
    return JsonResponse(entries_serializers.data, safe = False)

"""
{
    "title":
    "description":
}
"""
@api_view(['POST'])
def add_to_do(request):
    data = JSONParser().parse(request)
    data["uid"] = getStamp()
    td_serializer = ToDoSerializer(data = data)
    if td_serializer.is_valid():
        td_serializer.save()
        return JsonResponse(td_serializer.data, status = status.HTTP_201_CREATED)
    return JsonResponse(td_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_todo(request):
    data = JSONParser().parse(request)
    try: 
        entry = Entry.objects.get(pk = data["uid"])
    except:
        return (JsonResponse({'message': 'Entry does not exist'}))
    entry.delete()
    return JsonResponse({'message': 'Deleted'}, status = status.HTTP_204_NO_CONTENT)
    
