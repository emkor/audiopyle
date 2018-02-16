from django.conf.urls import url
from storage.vampy_plugin import views

urlpatterns = [
    url(r'^plugin-category/$', views.vampy_plugin_category_list),
    url(r'^plugin-category/(?P<pk>[0-9]+)/$', views.vampy_plugin_category_detail),
]
