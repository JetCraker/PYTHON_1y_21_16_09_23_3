from django.urls import path
from .views import add_and_save, dashboard, HelloView, BbIndexView, BbByRubricView

app_name = 'bboard'
urlpatterns = [
    path('', BbIndexView.as_view(), name='index'),
    path('rubric/<int:rubric_id>/', BbByRubricView.as_view(), name='by_rubric'),
    path('add/', add_and_save, name='add'),
    path('dashboard/', dashboard, name="dashboard"),
    path('hello/', HelloView.as_view(), name='hello'),
]

