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

from apiclient.http import MediaFileUpload
from apiclient import errors
from apiclient.http import MediaFileUpload

import requests

# Create your views here.
# # Create your views here.
# def SaveProfile(request):
#     text = """<h1>file saved !</h1>"""
#     return HttpResponse(text)

ROOT = os.path.dirname(os.path.abspath(__file__))
# folder_id = '0B6TQGqGzyC5rZ2NBUktISDRJRnc'
app_id = "AKfycbzXBfABkM_7AFKFcelFcfPshNSX5GrjAr2TNefYmYFYuDrd-OA"


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
            folder_id = "0B6TQGqGzyC5rZmFBZFdaZ2NfcnM"

        # if not isinstance(image.pic, ImageField :
        if "picture" in imageForm.cleaned_data:
            image.pic = imageForm.cleaned_data["picture"]
            fname, image_link, service = getLink(image.pic.url, image, folder_id)
        elif image.url != "":
            fname, image_link, service = getLink(img.url, image, folder_id)
        else:
            return render(request, 'prototype.html', {
                "folderid": request.session["folderid"],
                "returnText": request.session["returnText"],
            })
        
        if image.hw:
            text_output = str(text_recognition(image_link))
        else:
            text_output = str(ocr(image_link))

        # TODO:
        for char in text_output:
            try:
                char.encode("cp1521")
            except:
                char = "?"
        
        request.session["returnText"] = text_output

        prefix = "https://script.google.com/a/macros/student.monash.edu/s/"
        infix = "/exec?id="
        suffix = "&data="

        results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        create = True
        if items:
            for item in items:
                if "mimeType" in item.keys():
                    if "mimeType" == "application/vnd.google-apps.document":
                        create = False
                        # doc_link = prefix + folder_id + infix + item["id"] + suffix + text_output
                        doc_link = prefix + app_id + infix + item["id"] + suffix + text_output
                # print('{0} ({1})'.format(item['name'], item['id']))
        if create:
            media_body = MediaFileUpload("notes", mimetype="application/vnd.google-apps.document", resumable=True)
            body = {
                'title': "Shared Notes",
                'description': "Automated note generation",
                'mimeType': "application/vnd.google-apps.document"
            }
            # Set the parent folder.
            body['parents'] = [{'id': folder_id}]

            try:
                file = service.files().insert(
                    body=body,
                    media_body=media_body).execute()
            except errors.HttpError:
                print('An error occurred: %s' % error)

            # doc_link = prefix + folder_id + infix + file["id"] + suffix + text_output
            doc_link = prefix + app_id + infix + file["id"] + suffix + text_output
        
        r = requests.get(doc_link)

        return render(request, 'prototype.html', {
            "folderid": request.session["folderid"],
            "returnText": request.session["returnText"],
        })