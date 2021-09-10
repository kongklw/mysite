from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer
# from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.throttling import UserRateThrottle


# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# class UserList(APIView):
#
#     def get(self, request):
#         print('users get')
#
#         usernames = [username for username in User.objects.all()]
#         print(usernames)
#
#         return Response(usernames)


# Create your views here.

# 创建一个请求限制的视图


class FileUploadView(APIView):

    def post(self, request):
        file = request.data['file']
        print(request.stream)
        print(file)

        return Response({'msg': '上传成功'})


class OnceRequestDay(UserRateThrottle):
    rate = '2/m'


@api_view(http_method_names=['GET', 'POST'])
@throttle_classes([OnceRequestDay])
def once_request(request):
    if request.method == 'POST':
        return Response({'method': 'post', 'msg': request.data})

    return Response({'method': 'get', 'msg': 'hello world'})


# 类视图方式
'''
实现功能方法有
1、查询所有snippets的列表
2、实现post添加数据
3、实现get 指定获取记录
4、put修改内容
5、delete删除记录
'''


class SnippetsList(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get(self, request):

        # print(request.user)
        # print(request.authenticators)
        # print('-----------')
        # print('data', request.data)
        # print('query params', request.query_params)
        # print('parsers', request.parsers)
        # print('accepted_renderer', request.accepted_renderer)
        # print('accepted_media_type', request.accepted_media_type)
        # print('user', request.user)
        # print('auth', request.auth)
        # print('authenticators', request.authenticators)
        # print('method', request.method)
        # print('content type', request.content_type)
        # print('stream', request.stream)
        # # print('meta', request.META)
        # print('session', request.session)
        snippet = Snippet.objects.all()
        serializer = SnippetSerializer(snippet, many=True)
        print(serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class SnippetsDetail(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    # 在一个函数之中可以先把 snippet 实例化出来，然后后续接着用
    # 在一个类的方法中，如何使用，函数，还是重复写.
    @staticmethod
    def obtain_snippet(pk):
        try:
            snippet = Snippet.objects.get(pk=pk)
            return snippet
        except:

            return False

    def get(self, request, pk):
        print(11111)
        snippet = self.obtain_snippet(pk=pk)
        if not snippet:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk):

        # data = JSONParser().parse(request)
        data = request.data

        snippet = self.obtain_snippet(pk=pk)
        if not snippet:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        snippet = self.obtain_snippet(pk=pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 函数视图方式
"""
class JSONResponse(HttpResponse):
    # 重写jsonresponse 类的输出为序列化格式
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
@api_view(['GET','POST'])
def snippet_list(request):
    if request.method == 'GET':
        snippet = Snippet.objects.all()
        print(snippet)
        for item in snippet:
            print(item.title, item.code, item.created)
        serializer = SnippetSerializer(snippet, many=True)

        # return JSONResponse(serializer.data)
        return Response(serializer.data)

    elif request.method == 'POST':

        data = JSONParser().parse(request)

        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def snippet_detail(request, pk):
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # 更新 update 方式 是否还需要传入serializer.ata
        # 1/解析出来传入的参数
        # 2/序列化 该pk 的 snippet 对象 和 data数据
        # 3、更新也是保存。直接用save
        data = JSONParser().parse(request)

        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            # serializer.update(snippet, serializer.data)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return JSONResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        # orm 如何删除一个模型类对象的数据
        # 答案 直接实例化的snippet.delete()
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

"""
