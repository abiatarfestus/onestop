from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import (
    EnglishWord,
    OshindongaWord,
    WordDefinition,
    DefinitionExample,
    OshindongaIdiom,
    OshindongaPhonetic,
)

# Register your models here.

class WordDefinitionAdmin(SimpleHistoryAdmin):
    # list_display = ["id", "name", "status"]
    # history_list_display = ["status"]
    # search_fields = ['name', 'user__username']
    date_hierarchy = "time_added"
    # inlines = [ReviewInline]
    list_display = ("word_pair", "part_of_speech", "id")
    list_filter = ("part_of_speech",)
    ordering = ("word_pair",)
    raw_id_fields = ("word_pair", "synonyms",)
    # prepopulated_fields = {"slug": ("title",)}
    search_fields = ("word_pair__word", "word_pair__english_word__word",)

class EnglishWordAdmin(SimpleHistoryAdmin):
    date_hierarchy = "time_added"
    list_display = ("word", "id")
    ordering = ("word",)
    search_fields = ("word", )

class OshindongaWordWordAdmin(SimpleHistoryAdmin):
    date_hierarchy = "time_added"
    list_display = ("english_word", "word", "word_case", "id")
    list_filter = ("word_case",)
    ordering = ("english_word",)
    raw_id_fields = ("english_word",)
    search_fields = ("english_word__word", "word",)

class DefinitionExampleAdmin(SimpleHistoryAdmin):
    date_hierarchy = "time_added"
    list_display = ("definition", "id")
    ordering = ("definition",)
    raw_id_fields = ("definition",)
    search_fields = ("definition__word_pair__word", "definition__word_pair__english_word__word",)

admin.site.register(EnglishWord, EnglishWordAdmin)
admin.site.register(OshindongaWord, OshindongaWordWordAdmin)
admin.site.register(WordDefinition, WordDefinitionAdmin)
admin.site.register(DefinitionExample, DefinitionExampleAdmin)
admin.site.register(OshindongaIdiom, SimpleHistoryAdmin)
admin.site.register(OshindongaPhonetic, SimpleHistoryAdmin)

# admin.site.register(EnglishWord, SimpleHistoryAdmin)
# admin.site.register(OshindongaWord, SimpleHistoryAdmin)
# admin.site.register(WordDefinition, SimpleHistoryAdmin)
# admin.site.register(DefinitionExample, SimpleHistoryAdmin)
# admin.site.register(OshindongaIdiom, SimpleHistoryAdmin)
# admin.site.register(OshindongaPhonetic, SimpleHistoryAdmin)
