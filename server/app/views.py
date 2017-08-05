from django.shortcuts import render
from django.core.files import File
import os
from django import forms
from app.models import Profile, someImage
from django.http import HttpResponse
import uuid

from app.drivetest import main

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
        return render(request, 'uploadform.html')
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

        main("C:/Users/persi/Desktop/uniHack/server/app/img/" + uuuuuid + imgType)

        # upload to gdrive

        # get addr of file

        # call text(url)

        return HttpResponse("""<h1>file saved !</h1>""")
