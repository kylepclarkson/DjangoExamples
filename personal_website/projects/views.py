from django.shortcuts import render

from projects.models import Project

# Create your views here.

def project_index(request):
    ''' Get all projects. '''
    projects = Project.objects.all()
    context = {
        'projects': projects
    }

    return render(request, 'project_index.html', context)

def project_detail(request, pk):
    ''' Get project by primary key pk. '''
    project = Project.objects.get(pk=pk)
    context = {
        'project': project
    }

    return render(request, 'project_detail.html', context)



