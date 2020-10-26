from django.shortcuts import render
from django.http import HttpResponse

def home(req):
    return HttpResponse("<H1> Hello, World!</H1>")
