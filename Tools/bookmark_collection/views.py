from asyncio.log import logger
import logging
from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from bookmark_collection.models import Entry
from bookmark_collection.serializers import EntrySerializer
from rest_framework.decorators import api_view
from pyshorteners import Shortener

from hashlib import md5
from getTimeStamp import getStamp

# Create your views here.

headers =  {"Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,HEAD,OPTIONS,POST,PUT",
            "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept, Authorization"}


"""
{
    "uid": [integer](not explicitly required),
    "hash": [char],
    "url": [char],
    "title": [char],
    "description": [char]
}
"""
@api_view(['POST'])
def add_entry(request):
    entry_data = JSONParser().parse(request)
    url = entry_data['url']
    hash = md5(url.encode('utf-8')).hexdigest()
    entry_data["hash"] = hash
    entry_data["uid"] = getStamp()
    if (len(Entry.objects.filter(hash = hash)) != 0):
        logging.error('Entry: ' + hash + ' already exist')
        return JsonResponse({'message': 'Entry already exist'}, status = status.HTTP_400_BAD_REQUEST) 
    entry_serializer = EntrySerializer(data = entry_data)
    if entry_serializer.is_valid():
        entry_serializer.save()
        logger.debug(entry_serializer.data)
        return JsonResponse(entry_serializer.data, status = status.HTTP_201_CREATED)
    # return JsonResponse(entry_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    logger.error(entry_serializer.errors)
    return JsonResponse(entry_serializer.errors, status = status.HTTP_400_BAD_REQUEST, safe = False)

@api_view(['POST'])
def add_entries(request):
    entries_data = JSONParser().parse(request)
    entries_serializer = EntrySerializer(data = entries_data, many = True)
    if entries_serializer.is_valid():
        entries_serializer.save()
        return JsonResponse(entries_serializer.data, status = status.HTTP_201_CREATED, safe = False)
    return JsonResponse(entries_serializer.errors, status = status.HTTP_400_BAD_REQUEST, safe = False)
    # for data in request.data:
    #     entry_data = JSONParser().parse(data)
    #     entry_serializer = EntrySerializer(data = entry_data)
    #     if entry_serializer.is_valid():
    #         entry_serializer.save()
    

@api_view(['GET'])
def list_bookmark(request):
    entris = Entry.objects.all()
    entris_seriazlier = EntrySerializer(entris, many = True)
    return JsonResponse(entris_seriazlier.data, safe = False)

@api_view(['DELETE'])
def delete_entry(request):
    pk = request.data['uid']
    try:
        entry = Entry.objects.get(pk = pk)
    except:
        return JsonResponse({'message': 'Entry does not exist'})
    entry.delete()
    return JsonResponse({'message': 'Deleted'})

"""
{
    "uid": [integer](explicitly required),
    "hash": [char],
    "url": [char],
    "title": [char],
    "description": [char]
}
"""
@api_view(['PUT'])
# 由于使用hash作为primary key，导致继承DRF的serializer无法对hash field进行update操作（会生成一个新的记录）
# 使用部分数据进行update的时候要加上参数partial = True，否则无法调用update()
def update__d(request):
    data = JSONParser().parse(request)
    pk = data['uid']
    try:
        entry = Entry.objects.get(pk = pk)
    except:
        return JsonResponse({'message': 'Entry does not exist'})
    if ('url' in data):
        hash = md5(data['url'].encode('utf-8')).hexdigest()
        data['hash'] = hash
    entry_serializer = EntrySerializer(entry, data = data, partial=True, many = False)
    if entry_serializer.is_valid():
        entry_serializer.save()
        return JsonResponse(entry_serializer.data)
    logging.debug(entry_serializer.data)
    return JsonResponse(entry_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_entry(request):
    data = JSONParser().parse(request)
    hash = data['hash']
    try:
        entry = Entry.objects.get(pk = hash)
        logging.debug(hash)
    except:
        return JsonResponse({'message': 'Entry does not exist'})
    if ('url' in data):
        new_hash = md5(data['url'].encode('utf-8')).hexdigest()
        data['hash'] = new_hash
    try:
        Entry.objects.filter(pk = hash).update(**data)
    except:
        return JsonResponse({'message': 'duplicated'})
    try:
        hash = new_hash
    finally:
        entry = Entry.objects.get(pk = hash)
        logging.debug(entry)
        entry_serializer = EntrySerializer(entry)
        return JsonResponse(entry_serializer.data)

"""
{
    "begin": [int],
    "step": [int],
    # "tag":
}
"""
@api_view(['GET'])
def slice_(request):
    data = JSONParser().parse(request)
    begin = data["begin"]
    step = data["step"]
    # 融合标签搜索是否需要对entry使用filter?或者说对[标签]<->[Entry]使用filter即可
    # DFS标签，取得所有子类，对[标签]<->[Entry]通过[tag]过滤，取得[uid]组
    # 传入uid组[]
    dic = {}
    query = Entry.objects.filter(**dic)
    end = min(len(query), begin + step)
    begin = min(len(query), begin)
    entries = query[begin : end]
    entries_serializer = EntrySerializer(entries, many = True)
    return JsonResponse(entries_serializer.data, safe = False)

@api_view(['POST'])
def add_bl(request):
    request_data = JSONParser().parse(request)
    link = request_data["url"]
    s = Shortener()
    ex_link = s.tinyurl.expand(link)
    request_data["url"] = ex_link.split("?")[0]
    hash = md5(request_data["url"].encode('utf-8')).hexdigest()
    request_data["hash"] = hash
    request_data["uid"] = getStamp()
    # return JsonResponse({"message": "done"}, status = status.HTTP_200_OK)
    if (len(Entry.objects.filter(hash = hash)) != 0):
        logging.error('Entry: ' + hash + ' already exist')
        return JsonResponse({'message': 'Entry already exist'}, status = status.HTTP_400_BAD_REQUEST) 
    entry_serializer = EntrySerializer(data = request_data)
    if entry_serializer.is_valid():
        entry_serializer.save()
        return JsonResponse(entry_serializer.data, status = status.HTTP_201_CREATED)
    return JsonResponse(entry_serializer.errors, status = status.HTTP_400_BAD_REQUEST)