from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from users.models import User


class UsersViewSet(ModelViewSet):
    model = User