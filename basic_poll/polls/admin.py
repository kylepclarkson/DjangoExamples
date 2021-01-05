from django.contrib import admin

from .models import Question, Choice

# Register your models here.
# admin.site.register(Question)
# admin.site.register(Choice)

class ChoiceInline(admin.TabularInline):
    # Create 3 inline choices using Choice Model.
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    """ Register models using customization via class. """

    # Create fields (first value string naming field.)
    fieldsets = [
        (None,              {'fields': ['question_text']}),
        ('Date information',{'fields': ['pub_date']}),
    ]
    list_display = ('question_text', 'pub_date', 'was_published_recently')

    inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)


