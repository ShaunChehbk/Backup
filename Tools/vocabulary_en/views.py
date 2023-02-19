from asyncio.log import logger
from itertools import count
# import logging
from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

from vocabulary_en.models import Word
from vocabulary_en.serializers import WordSerializer, TouchHistorySerializer, InterpretationSerializer
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

import random
import decimal
# import json
from getTimeStamp import getStamp
# Create your views here.

def makeNew(data):
    data["uid"] = getStamp()
    if (not "rating" in data):
        data["rating"] = 1
    if (not "count" in data):

        data["count"] = 1

"""
{"word": [char], "rating": [float]} for updating word
{"word": [char]} for adding new word
"""
"""
TO-DO: override serializer.create() and update() for partial data constructing
"""
@api_view(['POST'])
def touch(request):
    words_data = JSONParser().parse(request)
    # 用于批量导入，不建议经常使用
    if (isinstance(words_data, list)):
        for data in words_data:
            makeNew(data)
        words_serializer = WordSerializer(data = words_data, many = True)
        if words_serializer.is_valid():
            words_serializer.save()
            return JsonResponse(words_serializer.data, status = status.HTTP_201_CREATED, safe = False)
        return JsonResponse(words_serializer.errors, status = status.HTTP_400_BAD_REQUEST, safe = False)

    else:
        try:
            w = words_data["word"]
            word = Word.objects.get(word = w)
            # logger.debug(word.rating)
            # logger.debug(word.uid)
            
            cur_rate = decimal.Decimal(words_data["rating"])
            # logger.debug(cur_rate)
            last_rate = word.rating
            last_count = word.count
            d = {
                "uid": getStamp(),
                "touchee": word.uid,
                "rate": cur_rate
            }
            touch_serializer = TouchHistorySerializer(data = d)
            if touch_serializer.is_valid():
                # logger.debug(touch_serializer.errors)
                # logger.debug(touch_serializer.validated_data)
                touch_serializer.save()
            # word.rating = words_data["rating"] * word.count + words_data["rating"] / (word.count + 1)
            # word.rating = float(word.rating * word.count) + words_data["rating"] / (word.count + 1)
            word.rating = (last_rate * last_count +  cur_rate)/ (last_count + decimal.Decimal('1'))


            word.count += 1
            word.save()
            word = Word.objects.get(word = w)
            return JsonResponse(WordSerializer(word).data)
        except ObjectDoesNotExist:
            makeNew(words_data)
            words_serializer = WordSerializer(data = words_data)
            logger.debug(words_data)
            if words_serializer.is_valid():
                words_serializer.save()
                uid = words_data["uid"]
                logger.debug(uid)
                d = {
                    "uid": getStamp(),
                    "touchee": uid,
                    "rate": 0
                }
                touch_serializer = TouchHistorySerializer(data = d)
                if touch_serializer.is_valid():
                    # logger.debug(touch_serializer.data)
                    touch_serializer.save()
                logger.debug(touch_serializer.errors)
                return JsonResponse(words_serializer.data, status = status.HTTP_201_CREATED, safe = False)
            return JsonResponse(words_serializer.errors, status = status.HTTP_400_BAD_REQUEST, safe = False)

@api_view(['GET'])
def list_words(request):
    words = Word.objects.all()
    words_serializer = WordSerializer(words, many = True)
    return JsonResponse(words_serializer.data, safe = False)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes((IsAuthenticated,))
def get_sample(request):
    words = Word.objects.all()
    sample = random.sample(list(range(len(words))), 10)
    res = []
    for i in sample:
        res.append(WordSerializer(words[i]).data)
    # logging.debug(res)
    return JsonResponse(res, safe = False)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes((IsAuthenticated,))
def get_untouched(request):
    words = Word.objects.filter(count__exact = 0)
    sample = random.sample(list(range(len(words))), 10)
    res = []
    for i in sample:
        res.append(WordSerializer(words[i]).data)
    return JsonResponse(res, safe = False)

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes((IsAuthenticated,))
def add_int(request):
    data = JSONParser().parse(request)
    data["uid"] = getStamp()
    int_serializer = InterpretationSerializer(data = data)
    if int_serializer.is_valid():
        int_serializer.save()
        return JsonResponse(int_serializer.data, status = status.HTTP_201_CREATED)
    return JsonResponse(int_serializer.errors, status = status.HTTP_400_BAD_REQUEST)