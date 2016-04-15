from django.conf.urls import include, url

urlpatterns = [
   url(r'^polls/', include('polls.urls', namespace='polls')),
]
