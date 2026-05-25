from django.contrib import admin
from .models import Album, Photo


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'get_photo_count', 'created_at')
    list_filter = ('owner', 'created_at')
    search_fields = ('name', 'description', 'owner__username')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Album Information', {
            'fields': ('name', 'description', 'owner')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'album', 'owner', 'uploaded_at')
    list_filter = ('owner', 'album', 'uploaded_at')
    search_fields = ('title', 'description', 'owner__username', 'album__name')
    readonly_fields = ('uploaded_at', 'updated_at')
    fieldsets = (
        ('Photo Information', {
            'fields': ('title', 'description', 'image', 'album', 'owner')
        }),
        ('Timestamps', {
            'fields': ('uploaded_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
