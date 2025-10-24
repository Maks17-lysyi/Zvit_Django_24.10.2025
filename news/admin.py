from django.contrib import admin
from .models import News, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
	search_fields = ('name',)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
	list_display = ('title', 'league', 'created_at', 'is_featured')
	list_filter = ('league', 'is_featured')
	search_fields = ('title', 'summary')
	prepopulated_fields = { 'slug': ('title',) }
	autocomplete_fields = ('league',)
	filter_horizontal = ('tags',)
