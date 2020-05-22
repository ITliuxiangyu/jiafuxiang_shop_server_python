from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse

from urllib import parse,request

import requests
from django.core.files.uploadedfile import InMemoryUploadedFile

from django.db import connection

import json


import string

import hashlib

from django.views.decorators.csrf import csrf_exempt

from django.core.cache import cache


def xxxxx(request):
    return HttpResponse("woshi  data shuju")