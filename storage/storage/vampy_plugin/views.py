from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from storage.vampy_plugin.models import VampyPluginCategory
from storage.vampy_plugin.serializers import VampyPluginCategorySerializer


@csrf_exempt
def vampy_plugin_category_list(request):
    if request.method == 'GET':
        snippets = VampyPluginCategory.objects.all()
        serializer = VampyPluginCategorySerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = VampyPluginCategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def vampy_plugin_category_detail(request, pk):
    try:
        snippet = VampyPluginCategory.objects.get(pk=pk)
    except VampyPluginCategory.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = VampyPluginCategorySerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = VampyPluginCategorySerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)
