from django.conf.urls import url
from django.contrib import admin

from .views import ActorView

urlpatterns = [
    url(r'^(?i)actor/(?P<name>[a-zàâçéèêëîïôûùüÿñæœ-]{0,75})', ActorView.as_view()),
    url(r'^admin/', admin.site.urls),
]
