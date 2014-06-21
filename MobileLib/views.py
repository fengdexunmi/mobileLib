#coding=utf8
from datetime import datetime, timedelta
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from MobileLib.forms import PostNoteForm
from MobileLib.models import Book, Record, Note


# Create your views here.
def signup(request):
    """注册"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()
    return render_to_response('signup.html', {'form': form}, context_instance=RequestContext(request))


def signin(request):
    """登录"""
    state = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
        else:
            state = '用户名或者密码出错'

    return render_to_response('signin.html', {'state':state}, context_instance=RequestContext(request))


def logout(request):
    """退出"""
    auth.logout(request)
    return HttpResponseRedirect('/signin')


def index(request):
    """主页"""
    if request.user.is_authenticated() is True:  # 已验证用户
        book_reading = Book.objects.filter(owner=request.user)  # 在读的图书
        return render_to_response('index.html',
                                  {
                                      'book_reading': book_reading,
                                      'book_returned_set': get_book_returned(request),
                                      'user': request.user,
                                  },
                                  context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/signin')


def show_book_by_isbn(request, isbn):
    """根据ISBN获取书目"""
    if request.user.is_authenticated() is True:
        book_by_isbn = Book.objects.get(isbn=isbn)
        book_reading = Book.objects.filter(owner=request.user)
        book_returned_set = get_book_returned(request)
        last_return_date = book_by_isbn.borrow_date + timedelta(days=15)

        if not book_reading and not book_returned_set:
            return HttpResponseRedirect('/')

        if request.method == 'POST':  # 发表笔记
            form = PostNoteForm(request.POST)
            if form.is_valid():
                Note.objects.create(title=form.cleaned_data['title'],
                                    writer=request.user,
                                    book_related=book_by_isbn,
                                    content=form.cleaned_data['content'])

        else:
            form = PostNoteForm()

        return render_to_response('show_book.html',
                                  {
                                      'book_by_isbn': book_by_isbn,
                                      'user': request.user,
                                      'book_reading': book_reading,
                                      'book_returned_set': book_returned_set,
                                      'book_note': show_note(request, isbn),
                                      'read_time': has_read_time(request, isbn),
                                      'last_return_date': last_return_date,
                                      'form': form,
                                  },
                                  context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')


def get_book_returned(request):
    """获取当前用户的借书记录"""
    book_returned = Record.objects.filter(reader=request.user, status=0)  # 已还的图书
    book_returned_set = []
    for book in book_returned:
        book_returned_set.append(book.book)

    return book_returned_set


def has_read_time(request, isbn):
    book_returned_by_isbn = Record.objects.filter(book__isbn=isbn, reader=request.user, status=0)
    time_list = []
    for book in book_returned_by_isbn:
        time_list.append(book.borrow_date)
        time_list.append(book.rel_return_date)
    return time_list


def show_note(request, isbn):
    """获取笔记"""
    book = Book.objects.get(isbn=isbn)
    book_note = Note.objects.filter(writer=request.user, book_related=book)

    return book_note


def delete_note(request, isbn, note_id):
    """删除笔记
    @param request:
    @param note_id:
    """
    if request.user.is_authenticated() is True:
        note_queryset = Note.objects.filter(id=note_id, writer=request.user)
        if note_queryset:
            note_queryset.delete()

    return HttpResponseRedirect('/book/isbn/%s/' % isbn)


def edit_note(request, isbn, note_id):
    """
    编辑笔记
    @param request:
    @param isbn:
    @param note_id:
    @return:
    """
    note_edit = Note.objects.filter(id=note_id)
    if request.method == 'POST':
        form = PostNoteForm(request.POST)
        if form.is_valid():
            note_edit.update(title=form.cleaned_data['title'],
                             content=form.cleaned_data['content'],
                             write_date=datetime.now())
            return HttpResponseRedirect('/book/isbn/%s/#read_note' % isbn)
    else:
        form = PostNoteForm()

    return render_to_response('edit_note.html',
                              {
                                  'note_edit': note_edit,
                                  'form': form
                              },
                              context_instance=RequestContext(request))












