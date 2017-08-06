from django.shortcuts import render
from django.core.files import File
import os
from django import forms
from app.models import Profile, someImage
from django.http import HttpResponse
import uuid

from app.drivetest import main
from app.vision import ocr
from app.vision import text_recognition

from apiclient.http import MediaFileUpload
from apiclient import errors
from apiclient.http import MediaFileUpload
import urllib

import requests

# Create your views here.
# # Create your views here.
# def SaveProfile(request):
#     text = """<h1>file saved !</h1>"""
#     return HttpResponse(text)

ROOT = os.path.dirname(os.path.abspath(__file__))
# folder_id = '0B6TQGqGzyC5rZ2NBUktISDRJRnc'


class ProfileForm(forms.Form):
    picture = forms.ImageField()


def getLink(imgUrl, image, folder_id):
    imgType = imgUrl[imgUrl.rfind("."):]
    uuuuuid = str(uuid.uuid1())
    image.pic.save(uuuuuid + imgType, image.pic, False)

    saved = 1
    source = ROOT + "/img/" + uuuuuid + imgType
    fname = source[source.rfind("/")+1:]
    image_link, service = main(fname, folder_id, source)
    return fname, image_link, service

def index(request):
    saved = 0
    print("request received: " + request.method)
    if request.method == "GET":
        if "folderid" in request.session:
            return render(request, 'prototype.html', {"folderid": request.session["folderid"]})
        else:
            return render(request, 'prototype.html', {})
    elif request.method == "POST":
        # print(request.POST)
        imageForm = ProfileForm(request.POST, request.FILES)

        imageForm.is_valid()

        image = someImage()
        image.url = request.POST["imgurl"]
        image.fid = request.POST["folderid"]
        image.hw = "handwritten" in request.POST
        if request.POST["folderid"] != "":
            request.session["folderid"] = request.POST["folderid"]
        if "folderid" in request.session:
            folder_id = request.session["folderid"]
        else:
            print(request.POST)
            folder_id = "0B6TQGqGzyC5rZmFBZFdaZ2NfcnM"

        # if not isinstance(image.pic, ImageField :
        if "picture" in imageForm.cleaned_data:
            image.pic = imageForm.cleaned_data["picture"]
            fname, image_link, service = getLink(image.pic.url, image, folder_id)
        elif image.url != "":
            name = image.url[image.url.rfind("/")+1:]
            address = ROOT + "/img/" + name
            f = open(address, 'wb')
            f.write(urllib.request.urlopen(image.url).read())
            f.close()
            image_link, service = main(name, folder_id, address)
        else:
            return render(request, 'prototype.html', {
                "folderid": request.session["folderid"],
                "returnText": request.session["returnText"],
            })
        
        if image.hw:
            text_output = str(text_recognition(image_link))
        else:
            text_output = str(ocr(image_link))

        # for char in text_output:
        #     try:
        #         char.encode("cp1521")
        #     except:
        #         char = "?"
        
        request.session["returnText"] = text_output

        # prefix = "https://script.google.com/a/macros/student.monash.edu/s/"
        # infix = "/exec?id="
        # suffix = "&data="

        # with open(ROOT + "/txt/" + str(request.session.get_expiry_date())[:10] + ".txt", "a+") as handle:
            # handle.write(text_output)
        with open(ROOT + "/txt/" + request.POST["filename"] + ".txt", "a+") as handle:
            handle.write(text_output)

        file_metadata = {
            'name' : request.POST["filename"],
            # 'mimeType' : 'application/vnd.google-apps.document',
            'parents': [folder_id],
            'mimeType' : 'plain/text',
        }
        # media = MediaFileUpload(ROOT + '/txt/' + str(request.session.get_expiry_date())[:10] + ".txt",
        media = MediaFileUpload(ROOT + '/txt/' + request.POST["filename"] + ".txt",
                                mimetype='plain/text',
                                resumable=True)
        file = service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()
        print('File ID: %s' % file.get('id'))


        
        # except FileNotFoundError:
            # with open(ROOT + "/txt/" + fname[:fname.rfind(".")] + ".txt", "w+") as handle:
                # handle.write(text_output)

        return render(request, 'prototype.html', {
            "folderid": request.session["folderid"],
            "returnText": request.session["returnText"],
        })