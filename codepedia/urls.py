from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin

from core.views import RecentQuestionView, AnswerListView

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('', include('core.urls')),
    # path('account/', include('django.contrib.auth.urls')),

    url(r'^$', RecentQuestionView.as_view(), name="home"),
    path('questions/<int:pk>', AnswerListView.as_view(), name="question"),
    url(r'^account/', include('django.contrib.auth.urls')),
    url(r'^admin/', admin.site.urls)

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
