from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse


def main(request):

    if request.method == "GET":
        return render(request, 'login.html')
    else:
        return redirect(test)


def transfer(request):
    if request.method == "GET":
        return render(request,'transfer.html')
    else:
        acc_no = request.POST["acc_no"]
        print(acc_no)
        return render(request, 'transfer.html')

def test(request):
    if request.method == "POST":
        return render(request, 'test.html')
    else:
        return render(request, 'test.html')
