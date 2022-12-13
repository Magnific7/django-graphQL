from django.conf import settings
from django.urls import path,re_path
from . import views
from django.conf.urls.static import static


urlpatterns = [
    path('', views.Index, name='Index'),
    path('login', views.Login, name='Login'),
    path('reset', views.Cancel, name='reset'),
    path('history', views.History_page, name='history'),


]
if settings.DEBUG:
    from django.views.static import serve
    from django.conf.urls.static import static

    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)