from django.shortcuts import render 
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from.models import Todo
from django.urls import reverse_lazy


# Create your views here.

class TodoListView(ListView):
    model = Todo
    template_name = "Todo/list.html"
    context_object_name = "todos"

class TodoCreateView(CreateView):
  model = Todo
  template_name = "Todo/create.html"
  fields = ['title', 'description', 'is_active']
  success_url = reverse_lazy("todo_list")

class TodoUpdateView(UpdateView):
  model = Todo
  template_name = "Todo/update.html"
  fields = ['title', 'description', 'is_active']
  success_url = reverse_lazy("todo_list")

class TodoDeleteView(DeleteView):
  model = Todo
  template_name = "Todo/delete.html"
  success_url = reverse_lazy("todo_list")