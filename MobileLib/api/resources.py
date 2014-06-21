#coding=utf8

from django.conf.urls import url
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from tastypie import fields
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.exceptions import BadRequest
from tastypie.utils import trailing_slash
from tastypie.http import HttpForbidden, HttpUnauthorized
from MobileLib.models import Book, Record, Note


class OwnerResource(ModelResource):
    """借阅者"""
    class Meta:
        queryset = User.objects.all()
        fields = ['username', 'email']
        resource_name = 'owner'
        filtering = {
            'username': ['exact'],
        }
        allowed_methods = ['post']
        # list_allowed_methods = ['post']
        authentication = BasicAuthentication()
        authorization = Authorization()
        always_return_data = True

    # def get_object_list(self, request, *args, **kwargs):
    #     return User.objects.filter(username=request.user.username)

    def prepend_urls(self):
        params = (self._meta.resource_name, trailing_slash())
        return [
            url(r"^(?P<resource_name>%s)/signin%s$" % params, self.wrap_view('signin'), name="api_signin")
        ]

    def signin(self, request, **kwargs):
        """Authenticate a user, create a CSRF token for them, and return the user object as JSON."""
        self.method_check(request, allowed=['post'])
        data = self.deserialize(request, request.body,
                                format=request.META.get('CONTENT_TYPE', 'application/json'))
        username = data.get('username', '')
        password = data.get('password', '')
        if username == '' or password == '':
            return self.create_response(request, {
                'success': False,
                'error_message': 'Missing username or password'
            })

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                response = self.create_response(request, {
                    'success': True,
                    'id': user.id,
                    'username': user.username
                })
                # response.set_cookie("csrftoken", get_new_csrf_key())
                return response
            else:
                return self.create_response(request, {
                    'success': False,
                    'reason': 'disabled',
                }, HttpForbidden)
        else:
            return self.create_response(request, {
                'success': False,
                'error_message': 'Incorrect username or password',
            }, HttpUnauthorized)


class SignupResource(ModelResource):
    """注册"""
    class Meta:
        queryset = User.objects.all()
        fields = ['username', 'email']
        resource_name = 'signup'
        list_allowed_methods = ['post']
        detail_allowed_methods = ['post']
        authorization = Authorization()

    def obj_create(self, bundle, **kwargs):
        # REQUIRED_FIELDS = ('username', 'email', 'password')
        username = bundle.data['username']
        try:
            if User.objects.filter(username=username):
                raise BadRequest('此用户名已存在')
        except User.DoesNotExist:
            pass

        email = bundle.data['email']
        try:
            if User.objects.filter(email=email):
                raise BadRequest('此邮箱已被使用')
        except User.DoesNotExist:
            pass

        raw_password = bundle.data.pop('password')
        # if not validate_password(raw_password):
        #     raise BadRequest('输入的密码不合法')

        kwargs["password"] = make_password(raw_password)

        return super(SignupResource, self).obj_create(bundle, **kwargs)


class BookResource(ModelResource):
    owner = fields.ForeignKey(OwnerResource, 'owner')
    # reader = fields.ForeignKey(OwnerResource, 'reader')

    class Meta:
        queryset = Book.objects.all()
        resource_name = 'book'
        # authentication = BasicAuthentication()
        authorization = Authorization()
        allowed_methods = ['get', 'post', 'put', 'patch']
        filtering = {
            'owner': ALL_WITH_RELATIONS,
            'isbn': ['exact'],
            'is_borrowed': ['exact'],
        }

    def get_object_list(self, request, *args, **kwargs):
        is_get = (request.method == 'GET')
        if is_get is True:
            isbn = request.GET.get('isbn')
            if isbn is None:
                return Book.objects.filter(owner=request.user)
            else:  # 根据ISBN获取书籍
                return Book.objects.filter(isbn=isbn)
        else:
            return super(BookResource, self).get_object_list(request, *args, **kwargs)


class RecordResource(ModelResource):
    reader = fields.ForeignKey(OwnerResource, 'reader')
    book = fields.ForeignKey(BookResource, 'book', full=True)

    class Meta:
        queryset = Record.objects.all()
        resource_name = 'record'
        # authentication = BasicAuthentication()
        authorization = Authorization()
        filtering = {
            'reader': ALL_WITH_RELATIONS,
            'book': ALL_WITH_RELATIONS,
            # 'isbn': ['exact'],
            'status': ['exact'],
        }

    def get_object_list(self, request):
        return Record.objects.filter(reader=request.user)


class NoteResource(ModelResource):
    writer = fields.ForeignKey(OwnerResource, 'writer')
    book = fields.ForeignKey(BookResource, 'book_related')

    class Meta:
        queryset = Note.objects.all()
        resource_name = 'note'
        authorization = Authorization()
        filtering = {
            'book': ALL_WITH_RELATIONS,
            'writer': ALL_WITH_RELATIONS,
            # 'isbn': ['exact'],
        }

    def get_object_list(self, request):
        return Note.objects.filter(writer=request.user)