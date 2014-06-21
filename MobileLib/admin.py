#coding=utf8

from django.contrib import admin
from MobileLib.models import Book, Record, Note


# Register your models here.
class BookAdmin(admin.ModelAdmin):
    """图书管理"""
    search_fields = ['isbn', 'book_title', 'owner__username']
    list_display = ['book_title', 'book_author', 'book_publisher', 'is_borrowed', 'owner', 'borrow_date', 'return_date']
    list_filter = ['owner', 'is_borrowed']  # 添加过滤器


class RecordAdmin(admin.ModelAdmin):
    list_display = ['book', 'status', 'reader', 'borrow_date', 'def_return_date', 'rel_return_date']
    list_filter = ['reader']


class NoteAdmin(admin.ModelAdmin):
    list_filter = ['book_related', 'writer']

admin.site.register(Book, BookAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.register(Note, NoteAdmin)
