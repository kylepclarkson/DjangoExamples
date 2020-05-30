from django import forms
from courses.models import Course

# Form for students to enroll in a course.
# Will be used on CourseDetailView tto display enroll button.
class CourseEnrollForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(),
                                    widget=forms.HiddenInput)

