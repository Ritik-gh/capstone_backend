import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User

# Create your views here.

def index(request):
    return HttpResponse("<h1 style='font-family:sans-serif;color:#222'>Welcome to Worg, a feature rich bookmark manager.</h1>")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        data = json.loads(request.body)
        username = data["username"]
        password = data["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return JsonResponse({"msg": "Logged in successfully"},status=200)
        else:
            return JsonResponse({"message":"Invalid username and/or password." }, status = 400)
    else:
        return JsonResponse({"msg":"POST method required"}, status = 400)


def logout_view(request):
    logout(request)
    return HttpResponse(204)


def register(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data["username"]
        email = data["email"]

        # Ensure password matches confirmation
        password = data["password"]
        confirmation = data["confirmPassword"]
        if password != confirmation:
            return JsonResponse({"message","Passwords must match." }, status = 400)

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return JsonResponse({"message","Username already taken." }, status = 400)
        login(request, user)
        return JsonResponse({"msg":"Registered successfully"}, status=201)
    else:
        return JsonResponse({"msg":"POST method required"}, status = 400)