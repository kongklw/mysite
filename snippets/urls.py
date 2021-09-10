from django.conf.urls import url
from snippets import views
from rest_framework.schemas import get_schema_view

# urlpatterns = [
#     url(r'^snippets/$', views.snippet_list),
#     url(r'^snippets/(?P<pk>[0-9]+)$', views.snippet_detail)
# ]

schema_view = get_schema_view(title='pastebin api')

urlpatterns = [
    url('schema/$', schema_view),
    url(r'snippets/$', views.SnippetsList.as_view()),
    url(r'snippets/(?P<pk>[0-9]+)/$', views.SnippetsDetail.as_view()),
    url(r'once', views.once_request),
    url(r'upload', views.FileUploadView.as_view()),
    # url(r'^users/$', views.UserList.as_view()),
    # url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
]
