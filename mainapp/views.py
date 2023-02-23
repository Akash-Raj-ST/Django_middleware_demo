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
        return redirect(test)


def transfer(request):
    if request.method == "GET":
        return render(request, 'transfer.html')
    else:
        return render(request, 'transfer.html')


def test(request):
    if request.method == "GET":
        response = render(request, 'test.html')
        return response
    
    else:
        return render(request, 'test.html',)


