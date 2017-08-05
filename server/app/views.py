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



# Create your views here.
# # Create your views here.
# def SaveProfile(request):
#     text = """<h1>file saved !</h1>"""
#     return HttpResponse(text)

ROOT = os.path.dirname(os.path.abspath(__file__))
folder_id = '0B6TQGqGzyC5rZ2NBUktISDRJRnc'

class ProfileForm(forms.Form):
    picture = forms.ImageField()


def index(request):
    saved = 0
    print("request received: " + request.method)
    if request.method == "GET":
        return render(request, 'prototype.html')
    elif request.method == "POST":
        print(request.POST)
        imageForm = ProfileForm(request.POST, request.FILES)

        imageForm.is_valid()

        image = someImage()
        image.pic = imageForm.cleaned_data["picture"]
        image.url = request.POST["imgurl"]
        image.fid = request.POST["folderid"]
        image.hw = "handwritten" in request.POST

        # if request.session

        print(image.pic.url)
        imgType = image.pic.url[image.pic.url.rfind("."):]
        print(imgType)
        uuuuuid = str(uuid.uuid1())
        image.pic.save(uuuuuid + imgType, image.pic, False)
        print("URL after... ", "\\app\\img\\" + uuuuuid + imgType)

        print("saved")
        saved = 1
        source = ROOT + "/img/" + uuuuuid + imgType
        fname = source[source.rfind("/")+1:]
        image_link, service = main(fname, folder_id, source)

        # upload to gdrive
        # print(image_link)

        # get addr of file

        ocr_back = ocr(image_link)
        # print(ocr_back)
        # call text(url)

        text_output = str(ocr(image_link))

        prefix = "https://script.google.coma/macros/student.monash.edu/s/"

        suffix = "/exec?data="

        create_link = prefix + folder_id + suffix + text_output

            # print("text_out:", text_output)

        # textfile_path = ROOT + '/txt/' + fname[:fname.rfind(".")] + ".txt"

        # with open(textfile_path, "w") as handle:
            # handle.write(text_output)

        # file_metadata = {
            # 'name': fname[:fname.rfind(".")],
            # 'parents': [folder_id]
        # }
        # media = MediaFileUpload(textfile_path,
                                # mimetype='text/plain',
                                # resumable=True)
        # file = service.files().create(body=file_metadata,
                                            # media_body=media,
                                            # fields='id').execute()
        # print('Textfile ID: %s' % file.get('id'))

        return HttpResponse(
            """<h1>file uploaded!</h1>
               <p>Text: """ + text_output + "</p>"
        )
