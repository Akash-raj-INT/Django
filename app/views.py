from django.http import HttpResponse
from django.shortcuts import render

# def hello_world(request):
#     return HttpResponse("Hello World")

def add(request):
    a = int(request.GET.get('a', 0))
    b = int(request.GET.get('b', 0))
    result = a+b
    return HttpResponse(f"The sum of {a} and {b} is {result}")

def greet(request):
    name = request.GET.get('name','Guest')
    return HttpResponse(f"Hello, {name}")

def calc(request):
        num1 = int(request.GET.get('num1', 8))
        num2 = int(request.GET.get('num2', 6))
        operation = request.GET.get('operation')

        if operation == 'add':
            return HttpResponse(f"{num1 + num2}")
        elif operation == 'subtract':
           return HttpResponse(f"{num1 - num2}")
        elif operation == 'multiply':
           return HttpResponse(f"{num1 * num2}")
        elif operation == 'divide':
            if num2 != 0:
                return HttpResponse(f"{num1 / num2}")
                # http://localhost:8000/calc/?num1=15&num2=3&operation=divide
            else:
                return HttpResponse('Cannot divide by zero')
        else:
            return HttpResponse('Invalid operation')

def hello_template(request):
    name = 'i am akash'
    location = 'from Punjab'
    return render(request, 'app/home.html', {'name': name, 'location': location})

def user(request):
    name = request.GET.get('name', 'Guest')
    location = request.GET.get('location', 'Unknown')
    return render(request, 'app/home.html', {'name': name, 'location': location})

    # http://localhost:8000/user/?name=Akash&location=punjab
def addition(request):
    result = None
    if request.method == 'POST':
        num1 = int(request.POST.get('num1', 0))
        num2 = int(request.POST.get('num2', 0))
        result = num1 + num2
    return render(request, 'app/add.html', {'result': result})


  
