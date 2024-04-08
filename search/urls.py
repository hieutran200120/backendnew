from django.urls import path
from .views import GetNewView
from .views import GetView
urlpatterns = [
    path('', GetNewView.as_view(), name='get_new5'),
    path('get_new/', GetView.as_view(), name='get_new5'),
]