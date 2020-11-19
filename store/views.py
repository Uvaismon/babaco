from django.shortcuts import render


def home(req):
    return render(req, 'store/home.html',{'title':'Babaco-Home'})
