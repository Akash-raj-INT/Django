from django.urls import path
from .views import add, greet, calc, hello_template, user, addition
# from .views import hello_world

urlpatterns = [
    # path('', hello_world, name="hello")
    path('add/', add, name="add"),
    path('greet/', greet, name="greet"),
    path('calc/', calc, name="calc"),
    path('hello/', hello_template, name='hello'),
    path('user/', user, name='user'),
    path('addition/', addition, name='addition')
]
