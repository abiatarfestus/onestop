from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import EnglishWord, OshindongaWord, WordDefinition, DefinitionExample

# Register your models here.
admin.site.register(EnglishWord, SimpleHistoryAdmin)
admin.site.register(OshindongaWord, SimpleHistoryAdmin)
admin.site.register(WordDefinition, SimpleHistoryAdmin)
admin.site.register(DefinitionExample, SimpleHistoryAdmin)
