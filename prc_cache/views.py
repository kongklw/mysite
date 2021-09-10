from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import time
from functools import lru_cache


# Create your views here.
@lru_cache()
def obtain(num):
    time.sleep(1)
    return {'msg': 'ok'}


class PrcCache(APIView):

    def get(self, request):
        params = request.query_params

        name = params.get('name')
        age = params.get('age')
        hobby = params.get('hobby')
        ts = time.time()

        for i in [1, 2, 3, 3, 3, 3, 3, 2, 2, 1]:
            data = obtain(i)

        print(obtain.cache_info())
        # cache_clear 清除已经过缓的记录，下次接口请求，该函数的缓存内容将被消除。
        # obtain.cache_clear()
        td = time.time()
        wast_time = td - ts
        print('wast time', wast_time)

        return Response({'msg': 'ok'})
