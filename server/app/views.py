from django.shortcuts import render
from django.core.files import File
import os
from django import forms
from app.models import Profile, someImage
from django.http import HttpResponse
import uuid


# Create your views here.
# # Create your views here.
# def SaveProfile(request):
#     text = """<h1>file saved !</h1>"""
#     return HttpResponse(text)

class ProfileForm(forms.Form):
   name = forms.CharField(max_length = 100)
   picture = forms.ImageField()

def index(request):
    saved = 0
    print("request received: "+ request.method )
    if request.method == "GET":
        return render(request, 'uploadform.html')
    elif request.method == "POST":
        imageForm = ProfileForm(request.POST, request.FILES)

        if imageForm.is_valid():

            image = someImage()
            image.pic = imageForm.cleaned_data["picture"]
            print(image.pic.url)
            imgType = image.pic.url[image.pic.url.rfind("."):]
            print(imgType)
            image.pic.save(str(uuid.uuid1()) + imgType,image.pic, False)
            print("URL after... ", image.pic.url)
            print("saved")
            saved = 1
        else:
            imageForm = ProfileForm()


        #upload to gdrive

        #get addr of file

        #call text(url)


        return HttpResponse("""<h1>file saved !</h1>""")
