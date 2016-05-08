from django.conf.urls import url
#from django.views.generic import TemplateView

from .views import ActivateAction

urlpatterns = [
    url(r'activate/(?P<name>[-\w]+)/*$', ActivateAction.as_view()),
    ]
