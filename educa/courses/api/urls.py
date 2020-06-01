from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'courses'

router = routers.DefaultRouter()
# Register router for viewset with 'courses' prefix.
router.register('courses', views.CourseViewSet)

urlpatterns = [
    path('subjects/',
         views.SubjectListView.as_view(),
         name='subject_list'),
    path('subjects/<pk>/',
         views.SubjectDetailView.as_view(),
         name='subject_detail'),
    # path('courses/<pk>/enroll',
    #      views.CourseEnrollView.as_view(),
    #      name='course_enroll'), functionality replaces by router - URL is build dynamically using action name 'enroll'
    path('', include(router.urls))
]