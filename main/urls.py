from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path, path
from django.views.generic import TemplateView
# from background_task import Task
from . import functions


from main import views

urlpatterns = [
    re_path(r'^$', TemplateView.as_view(template_name='main/index.html'), name='home'),
    re_path(r'^api/crawl/', views.crawl, name='crawl'),
    path('api/showdata/', views.show_data, name='show_data')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# if not Task.objects.filter(verbose_name="crawl").exists():
#     functions.crawl(verbose_name="crawl")