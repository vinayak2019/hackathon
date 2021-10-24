from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('',views.create_db, name="create_db"),
    path('login/',views.login, name="login"),
    path('view_data/',views.view_data, name="view_data"),
    path('add_data/', views.add_data, name="add_data"),
    url(r'^ajax/insert$',views.insert_data)
]