from django.conf.urls import url

from .views import ActorView

urlpatterns = [
    url(r'^(?i)actor/(?P<name>[a-zàâçéèêëîïôûùüÿñæœ-]{0,75})', ActorView.as_view()),
]
