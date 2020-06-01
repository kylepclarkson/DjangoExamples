
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from ..models import Subject, Course
from .permissions import IsEnrolled
from .serializers import SubjectSerializer, CourseSerializer, CourseWithContentsSerializer

class SubjectListView(generics.ListAPIView):

    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class SubjectDetailView(generics.RetrieveAPIView):
    # will include URL param 'pk'
    queryset = Subject.objects.all()
    serializer_class =  SubjectSerializer

# Custom APIView that handles user enrollment of courses
# == Handled by CourseViewSet.
# class CourseEnrollView(APIView):
#
#     authentication_classes = (BasicAuthentication,)
#     # User must be authenticated to access view
#     permission_classes = (IsAuthenticated,)
#     # Enroll student into course.
#     def post(self, request, pk, format=None):
#         course = get_object_or_404(Course, pk=pk)
#         course.students.add(request.user)
#         return Response({'enrolled': True})

class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


    '''
    Add current user to the students many-to-many relationship. 
    '''
    @action(detail=True,
            methods=['POST'],
            authentication_classes=[BasicAuthentication,],
            permission_classes=[IsAuthenticated,])
    def enroll(self, request, *args, **kwargs):
        course = self.get_object()
        course.students.add(request.user)
        return Response({'enrolled': True})

    '''
    Get course contents, ensuring user is in course. 
    '''
    @action(detail=True,
            methods=['GET'],
            serializer_class=CourseWithContentsSerializer,
            authentication_classes=[BasicAuthentication],
            permission_classes=[IsAuthenticated, IsEnrolled])
    def contents(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)