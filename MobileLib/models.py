#coding=utf8

import datetime
import re
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Book(models.Model):
    """书籍"""
    STATUS_CHOICES = (
        (0, '在馆'),
        (1, '借出'),
        # (2, '预借'),
        # (3, '预还'),
    )

    def validate_pub_date(value):
        if not re.match(r'^\d{4}-(\d{2}|\d)$', value):
            raise ValidationError('出版日期格式为YYYY-m或者YYYY-mm')

    isbn = models.BigIntegerField(max_length=13, unique=True, verbose_name='ISBN编号')
    book_title = models.CharField(max_length=100, unique=True, verbose_name='书名')  # 书名不可重复
    book_author = models.CharField(max_length=30, verbose_name='作者')
    book_publisher = models.CharField(max_length=50, verbose_name='出版社')
    pub_date = models.CharField(max_length=10, validators=[validate_pub_date], verbose_name='出版日期')
    # book_thumb = models.ImageField(verbose_name='缩略图')
    thumb_url = models.URLField(verbose_name='缩略图')
    book_summary = models.TextField(verbose_name='摘要')
    owner = models.ForeignKey(User, default=lambda: User.objects.get(id=1), related_name='owner', verbose_name='拥有者')
    # reader = models.ForeignKey(User, blank=True, null=True, related_name='reader', verbose_name='借阅者')
    is_borrowed = models.IntegerField(choices=STATUS_CHOICES, default=0, verbose_name='图书状态')
    borrow_date = models.DateField(blank=True, editable=False, null=True, verbose_name='借出时间')
    return_date = models.DateField(blank=True, editable=False, null=True, verbose_name='归还时间')

    def __unicode__(self):
        return self.book_title

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.id is not None:
            if self.is_borrowed is 1:
                self.borrow_date = datetime.datetime.today()
                is_exist = Record.objects.filter(book=self, reader=self.owner, status=1)
                if not is_exist:
                    Record.objects.create(book=self,
                                          # isbn=self.isbn,
                                          # title=self.book_title,
                                          reader=self.owner,
                                          borrow_date=self.borrow_date,
                                          def_return_date=datetime.datetime.now()+timedelta(days=15),
                                          status=1)
            else:
                self.return_date = datetime.datetime.today()
                Record.objects.filter(book=self,
                                      # isbn=self.isbn,
                                      borrow_date=self.borrow_date,
                                      status=1).update(rel_return_date=datetime.datetime.now(), status=0)

        super(Book, self).save(force_insert, force_update)

    class Meta:
        verbose_name_plural = '图书'


class Record(models.Model):
    STATUS_CHOICES = (
        (0, '已还'),
        (1, '借出'),
    )
    # isbn = models.BigIntegerField(max_length=13, verbose_name='ISBN编号')
    # title = models.CharField(max_length=100, verbose_name='书名')
    book = models.ForeignKey(Book, verbose_name='对应的图书')
    reader = models.ForeignKey(User, db_index=True, verbose_name='借阅者')
    borrow_date = models.DateField(blank=True, verbose_name='借出日期')
    def_return_date = models.DateField(blank=True, verbose_name='理论归还日期')
    rel_return_date = models.DateField(blank=True, null=True, verbose_name='实际归还日期')
    status = models.IntegerField(choices=STATUS_CHOICES, verbose_name="图书状态")

    def __unicode__(self):
        return self.book.book_title

    class Meta:
        verbose_name_plural = "记录"


class Note(models.Model):
    """读书笔记"""
    title = models.CharField(max_length=50, verbose_name='笔记标题')
    writer = models.ForeignKey(User, verbose_name='作者')
    book_related = models.ForeignKey(Book, verbose_name='书籍')
    content = models.TextField(verbose_name='笔记内容')
    write_date = models.DateField(auto_now=True, verbose_name='写作时间')

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = '读书笔记'



