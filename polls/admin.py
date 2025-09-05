from django.contrib import admin
from .models import Question, Choice, Vote


class ChoiceInline(admin.TabularInline):  # Inline para meter opciones en la misma pantalla
    model = Choice
    extra = 2   # Muestra 2 inputs vacíos por defecto


class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "pub_date", "was_published_recently")
    list_filter = ["pub_date"]
    search_fields = ["question_text"]
    inlines = [ChoiceInline]


# Registro de modelos en el admin
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)  # opcional, así puedes ver Choices también por separado
admin.site.register(Vote)
