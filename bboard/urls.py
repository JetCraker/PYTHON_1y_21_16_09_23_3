from django.urls import path
from .views import (add_and_save, dashboard, HelloView, BbIndexView, BbByRubricView,
                    goiteen_list_view, DataPageView, HomePageView, AboutPageView)

app_name = 'bboard'

urlpatterns = [
    #path('', BbIndexView.as_view(), name='index'),
    path('rubric/<int:rubric_id>/', BbByRubricView.as_view(), name='by_rubric'),
    path('add/', add_and_save, name='add'),
    path('dashboard/', dashboard, name="dashboard"),
    path('hello/', HelloView.as_view(), name='hello'),
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('data/', DataPageView.as_view(), name='data'),
    path('list/', goiteen_list_view, name='item_list')
]

