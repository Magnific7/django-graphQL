from django.conf import settings
from django.urls import path,re_path
from . import views
from Django_graphQL_app.schema import schema
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
from graphene_file_upload.django import FileUploadGraphQLView

urlpatterns = [
    path('', views.Index, name='Index'),
    path('login', views.Login, name='Login'),
    path('reset', views.Cancel, name='reset'),
    path('history', views.History_page, name='history'),
    path('graphql/',
               csrf_exempt(FileUploadGraphQLView.as_view(graphiql=True,
               schema=schema)),name='graphql')

]

if settings.DEBUG:
    from django.views.static import serve
    from django.conf.urls.static import static

    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)