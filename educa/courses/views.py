from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.forms.models import modelform_factory
from django.apps import apps
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import  LoginRequiredMixin, PermissionRequiredMixin
from braces.views import CsrfExemptMixin, JSONRequestResponseMixin

from .models import Course, Module, Content
from .forms import ModuleFormSet


class OwnerMixin(object):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)

class OwnerEditMixin(object):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class OwnerCourseMixin(OwnerMixin,
                       LoginRequiredMixin, # Must be login, have sufficient permissions.
                       PermissionRequiredMixin):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')

class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    template_name = 'courses/manage/course/form.html'


class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'courses/manage/course/list.html'
    permission_required = 'courses.view_course'


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    permission_required = 'courses.add_course'


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    permission_required = 'courses.change_course'


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = 'courses/manage/course/delete.html'
    permission_required = 'courses/delete_course'


# For retrieving the courses of a single user.
class ManageCourseListView(ListView):
    model = Course
    template_name = 'courses/manage/course/list.html'

    # Retrieve courses for current user only.
    def get_queryset(self):
        querySet = super(ManageCourseListView, self).get_queryset()
        return querySet.filter(owner=self.request.user)

# This formset handles add, update, and delete of modules for specific course.
class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/formset.html'
    course = None

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course, data=data)

    def dispatch(self, request, pk):
        # Get course using id parameter of current user.
        self.course = get_object_or_404(Course,
                                        id=pk,
                                        owner=request.user)
        return super().dispatch(request, pk)

    # execute GET request.
    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course':self.course,
                                        'formset': formset})

    # execute POST request.
    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)

        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')

        return self.render_to_response({'course':self.course,
                                        'formset': formset})

# Allows the creation and update of a model's content(s).
class ContentCreateUpdateView(TemplateResponseMixin,  View):
    module = None
    model = None
    obj = None
    template_name = 'courses/manage/content/form.html'

    def get_model(self, model_name):
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='courses', model_name=model_name)

        return None

    def get_form(self, model, *args, **kwargs):
        # Build form excluding fields that are not content.
        Form = modelform_factory(model, exclude=['owner',
                                                 'order',
                                                 'created',
                                                 'updated'])

        return Form(*args, **kwargs)

    # Receives URL parameters and stores the corresponding module model and content object
    # as class attributes.
    def dispatch(self, request, module_id, model_name, id=None):
        self.module = get_object_or_404(Module, id=module_id, course__owner=request.user)

        self.model = self.get_model(model_name)

        if id:
            self.obj = get_object_or_404(self.model, id=id, owner=request.user)

        return super().dispatch(request, module_id, model_name, id)

    # Build model for Text,Video,Image, or File, or create new object if id is not set.
    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)

        return self.render_to_response({'form': form,
                                        'object': self.obj})

    # Build model form and save.
    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj, data=request.POST, files=request.FILES)

        # Create new form
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()

            # Create new object
            if not id:
                Content.objects.create(module=self.module, item=obj)

            # Save/update object.
            return redirect('module_content_list', self.module.id)

        return self.render_to_response({'form': form,
                                        'object': self.obj})

# View for deleting content
class ContentDeleteView(View):

    def post(self, request, id):
        content = get_object_or_404(Content,
                                    id=id,
                                    module__course__owner=request.user)

        module = content.module
        content.item.delete() # delete the content of the content.
        content.delete()        # delete the content object itself.
        return redirect('module_content_list', module.id)


class ModuleContentListView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/content_list.html'

    def get(self, request, module_id):
        module = get_object_or_404(Module,
                                   id=module_id,
                                   course__owner=request.user)

        return self.render_to_response({'module': module})

# View receives the new order of modules in JSON format.
class ModuleOrderView(CsrfExemptMixin,
                      JSONRequestResponseMixin,
                      View):

    def post(self, request):
        # For each module, reorder according to order.
        for id, order in self.request_json.items():
            Module.objects.filter(id=id, course__owner=request.user).update(order=order)

        return self.render_json_response({'saved': 'OK'})


# View receives the new order of content in JSON format.
class ContentOrderView(CsrfExemptMixin,
                      JSONRequestResponseMixin,
                      View):

    def post(self, request):
        # For each module, reorder according to order.
        for id, order in self.request_json.items():
            Content.objects.filter(id=id, course__owner=request.user).update(order=order)

        return self.render_json_response({'saved': 'OK'})
