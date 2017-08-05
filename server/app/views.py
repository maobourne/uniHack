from django.shortcuts import render
from django.core.files import File
import os
from django import forms
from app.models import Profile
from django.http import HttpResponse


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
        print("index...\n\n")
        return render(request, 'uploadform.html')
    elif request.method == "POST":
        print("post received")
        imageForm = ProfileForm(request.POST, request.FILES)
        print("got image form")

        if imageForm.is_valid():
            print("form is valid")
            profile = Profile()
            profile.name = imageForm.cleaned_data["name"]
            profile.picture = imageForm.cleaned_data["picture"]
            profile.picture.save(os.path.basename(profile.name), profile.picture)
            print("saved")
            saved = 1
        else:
            imageForm = ProfileForm()

        return HttpResponse("""<h1>file saved !</h1>""")
