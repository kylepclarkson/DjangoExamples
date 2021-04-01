from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import TaskSerializer
from .models import Task


@api_view(['GET'])
def apiOverview(request):
    """ Return an overview of the routes to use this api. """
    api_urls = {
        'List': 'task-list/',
        'Detail View': '/task-detail/<str:pk>/',
        'Create': '/task-create/',
        'Update': '/task-update/',
        'Delete': '/task-delete/<str:pk>',
    }

    return Response(api_urls)


@api_view(['GET'])
def taskList(request):
    """ Return all tasks """
    tasks = Task.objects.all()
    # serialize many (all) tasks.
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def taskDetail(request, pk):
    """ Return single task based on its id. """
    tasks = Task.objects.get(id=pk)
    # serialize single task.
    serializer = TaskSerializer(tasks, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def taskCreate(request):
    """ Create new task. """
    # request.data comes in json form.
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def taskUpdate(request, pk):
    """ Update existing task. """
    task = Task.objects.get(id=pk)
    # request.data comes in json form.
    serializer = TaskSerializer(instance=task, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def taskDelete(request, pk):
    task = Task.objects.get(id=pk)
    task.delete()

    return Response("Item deleted")
