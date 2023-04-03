from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse

from .models import Users


def main(request):

    if request.method == "GET":
        return render(request, 'login.html')
    else:
        username = request.POST['username']
        password = request.POST['password']

        user = Users(username=username,password=password)
        user.save()
        user_id = user.user_id
        request.session['user_id'] = user_id

        print("Inside developer views function:\n")
        print(username,password)

        return redirect(transfer)


def transfer(request):
    if request.method == "GET":
        return render(request, 'transfer.html')
    else:
        return redirect(success)


def test(request):
    if request.method == "GET":
        print("test view triggered")

        return render(request, 'test.html')
    
    else:
        return render(request, 'success.html',)
    

def success(request):
    if request.method == "GET":
        print("Success")
        return render(request, 'success.html')


