from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


# Create your views here.

class JSONResponse(HttpResponse):
    # 重写jsonresponse 类的输出为序列化格式
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def snippet_list(request):
    if request.method == 'GET':
        snippet = Snippet.objects.all()
        print(snippet)
        for item in snippet:
            print(item.title,item.code,item.created)
        serializer = SnippetSerializer(snippet, many=True)

        return JSONResponse(serializer.data)

    elif request.method == 'POST':

        data = JSONParser().parse(request)

        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)


@csrf_exempt
def snippet_detail(request, pk):
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return JSONResponse(serializer.data)

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
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        # orm 如何删除一个模型类对象的数据
        # 答案 直接实例化的snippet.delete()
        snippet.delete()
        return HttpResponse(status=204)
