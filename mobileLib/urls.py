from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout
from tastypie.api import Api
from MobileLib.api.resources import OwnerResource, BookResource, SignupResource, RecordResource, NoteResource

v1_api = Api(api_name='v1')
v1_api.register(OwnerResource())
v1_api.register(BookResource())
v1_api.register(SignupResource())
v1_api.register(RecordResource())
v1_api.register(NoteResource())
# v1_api.register(SigninResource())


admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mobileLib.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'MobileLib.views.index'),
    url(r'^accounts/login/$', login),
    url(r'^accounts/logout/$', logout),
    url(r'^signin/$', 'MobileLib.views.signin'),
    # url(r'^signin/$', 'django.contrib.auth.views.login'),
    url(r'^signup/$', 'MobileLib.views.signup'),
    url(r'^logout/$', 'MobileLib.views.logout'),
    url(r'^book/isbn/(?P<isbn>\d+)/$', 'MobileLib.views.show_book_by_isbn'),
    url(r'^note/delete/(?P<isbn>\d+)/(?P<note_id>\d+)/$', 'MobileLib.views.delete_note'),
    url(r'^note/edit/(?P<isbn>\d+)/(?P<note_id>\d+)/$', 'MobileLib.views.edit_note'),
    url(r'^api/', include(v1_api.urls)),

)
