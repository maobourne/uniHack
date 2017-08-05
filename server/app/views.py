from django.shortcuts import render
from django.core.files import File
import os
from django import forms
from app.models import Profile, someImage
from django.http import HttpResponse
import uuid

from app.vision import ocr
from app.drivetest import main
from app.vision import ocr

import json

# Create your views here.
# # Create your views here.
# def SaveProfile(request):
#     text = """<h1>file saved !</h1>"""
#     return HttpResponse(text)


class ProfileForm(forms.Form):
    name = forms.CharField(max_length=100)
    picture = forms.ImageField()


def index(request):
    saved = 0
    print("request received: " + request.method)
    if request.method == "GET":
        return render(request, 'prototype.html')
    elif request.method == "POST":
        imageForm = ProfileForm(request.POST, request.FILES)

        imageForm.is_valid()

        image = someImage()
        image.pic = imageForm.cleaned_data["picture"]
        print(image.pic.url)
        imgType = image.pic.url[image.pic.url.rfind("."):]
        print(imgType)
        uuuuuid = str(uuid.uuid1())
        image.pic.save(uuuuuid + imgType, image.pic, False)
        print("URL after... ", "\\app\\img\\" + uuuuuid + imgType)

        print("saved")
        saved = 1

        image_link = main(os.path.dirname(os.path.abspath(__file__)) + "/img/" + uuuuuid + imgType)

        # upload to gdrive
        print(image_link)

        # get addr of file

        ocr_back = ocr(image_link)
        print(ocr_back)
        # call text(url)

        text_output = str(ocr(image_link))



        return HttpResponse("""<h1>file saved !</h1><p>Text: """ + text_output + "</p>")
