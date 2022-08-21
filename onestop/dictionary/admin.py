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
    date_hierarchy = "time_added"
    # inlines = [ReviewInline]
    list_display = ("word_pair", "part_of_speech", "id")
    list_filter = ("part_of_speech",)
    ordering = ("word_pair",)
    raw_id_fields = (
        "word_pair",
        "synonyms",
        "plurals",
    )
    # prepopulated_fields = {"slug": ("title",)}
    search_fields = (
        "word_pair__word",
        "word_pair__english_word__word",
    )


class EnglishWordAdmin(SimpleHistoryAdmin):
    date_hierarchy = "time_added"
    list_display = ("word", "id")
    ordering = ("word",)
    search_fields = ("word",)


class OshindongaWordAdmin(SimpleHistoryAdmin):
    date_hierarchy = "time_added"
    list_display = ("english_word", "word", "word_case", "id")
    list_filter = ("word_case",)
    ordering = ("english_word",)
    raw_id_fields = ("english_word",)
    search_fields = (
        "english_word__word",
        "word",
    )


class DefinitionExampleAdmin(SimpleHistoryAdmin):
    date_hierarchy = "time_added"
    list_display = ("definition", "id")
    ordering = ("definition",)
    raw_id_fields = ("definition",)
    search_fields = (
        "definition__word_pair__word",
        "definition__word_pair__english_word__word",
    )

class OshindongaIdiomAdmin(SimpleHistoryAdmin):
    date_hierarchy = "time_added"
    list_display = ("word_pair", "oshindonga_idiom", "id")
    ordering = ("word_pair",)
    raw_id_fields = ("word_pair",)
    search_fields = (
        "word_pair__word",
        "word_pair__english_word__word",
    )


admin.site.register(EnglishWord, EnglishWordAdmin)
admin.site.register(OshindongaWord, OshindongaWordAdmin)
admin.site.register(WordDefinition, WordDefinitionAdmin)
admin.site.register(DefinitionExample, DefinitionExampleAdmin)
admin.site.register(OshindongaIdiom, OshindongaIdiomAdmin)
admin.site.register(OshindongaPhonetic, SimpleHistoryAdmin)

# admin.site.register(EnglishWord, SimpleHistoryAdmin)
# admin.site.register(OshindongaWord, SimpleHistoryAdmin)
# admin.site.register(WordDefinition, SimpleHistoryAdmin)
# admin.site.register(DefinitionExample, SimpleHistoryAdmin)
# admin.site.register(OshindongaIdiom, SimpleHistoryAdmin)
# admin.site.register(OshindongaPhonetic, SimpleHistoryAdmin)
