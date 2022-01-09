from django.http import HttpResponse
from django.shortcuts import render
from store.models import *
from django.core.mail import EmailMessage
from django.views.decorators.gzip import gzip_page
from django.http import StreamingHttpResponse
import cv2
import threading
import numpy as np

@gzip_page
def Home(request):

    global catt
    #catt=request.GET.get('cat')
    #catt=str(catt)
    #catts=catt.replace("\\","//")
    catt=request.GET.get('zara')
    catt=str(catt)
    #catt=catt.replace("\\","/")

    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        pass
    return render(request, 'app1.html')

#to capture video class
class VideoCamera(object):



    #def save_content(self,request):
    #    if request.method == 'POST':
     #       if 'URL' in request.POST:
     #           self.file_data = request.POST['URL']
    


    #def request_page(self,request):
    #    self.so=request.GET.get('{{x.photo.url}}')


    def __init__(self):
        self.video=cv2.VideoCapture(0)
        (self.grabbed,self.frame)=self.video.read()
        threading.Thread(target=self.update,args=()).start()


    def __del__(self):
        self.video.release()

    def get_frame(self):
        x=0
        y=0
        h=0
        w=0

        x_user=0
        y_user=0
        z_user=0
        l_img=0
        crop=0
        #path="/imageuploader/ + self.post_id"
        shoo="pant"
        noo="shirt"


        #use=str(catt.split('/')[0:-1])
        #use=str(use)
        cattt=catt + "/"
        dog=cattt.split('/')[:-1]
        lionn=dog[-1]
        lion=str(lionn)

        #sub=str('h'.join(use.split('.')[0:]))
        #sub=str(sub)

        
        check=catt.split('2F')
        check=check[-1]
        check=str(check)

        so=catt.rsplit('/',1)[1]


        done=catt[32:]



        face_cascade=cv2.CascadeClassifier('/home/lenovo/django_playground/shubs/store/views/haarcascade_frontalface_default.xml')
        ##eye_cascade=cv2.CascadeClassifier('views/haarcascade_eye.xml')
        eye_cascade=cv2.CascadeClassifier('/home/lenovo/django_playground/shubs/store/views/haarcascade_eye.xml')


        img=self.frame
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #_,jpeg=cv2.imencode('.jpg',gray)
        ##poww="/imageuploader" + catt
        ##poww="/home/lenovo/django_playground/shubs/uploads/products" + catt
        ###poww="/home/lenovo/django_playground/shubs/uploads/products/" + so
        ###poww=str(poww)
        #path='"/imageuploader/imageuploader/" + catt'
        #path=str(poww)
        #s_img = cv2.imread("/imageuploader/media/myimage/1_JZoBjTL.png")
        #s_img = cv2.imread("\\media\\myimage\\1_JZoBjTL.png")
           #s_img=cv2.imread("/imageuploader/media/myimage/1_JZoBjTL.png")
        ###s_img=cv2.imread(poww) 
        ####s_img=cv2.imread("/home/lenovo/django_playground/shubs/uploads/products/815qCLkD6RL._UL1500_.jpg") 
        ##s_img=cv2.imread("/home/lenovo/django_playground/shubs/uploads/products"+so)
        s_img=cv2.imread("/home/lenovo/django_playground/shubs/uploads/products"+done) 
        ##s_img=cv2.imread("/home/lenovo/django_playground/shubs/uploads/myimage/1.jpg") 
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            flag=1
            l_img = img
            x_onset = 3.2*w/s_img.shape[0]+z_user
            y_onset = 2.5*h/s_img.shape[1]+z_user
            x_offset = int(x - x_onset*200)+x_user
            y_offset = int(y + h + 15)+y_user
            u_offset=y_offset
            d_offset=2*u_offset

            ##if shoo in lion:
            ##if shoo in done:
            ##    y_offset=d_offset

            ##elif noo in lion:
            ##elif noo in done:
            ##    y_offset=u_offset    




            if x_offset<=0:
                xcut=abs(x_offset)
                x_offset=0
            else:
                xcut=0
            s_img = cv2.resize(s_img,(0,0),fx=x_onset,fy=y_onset)
            crop=s_img[0:l_img.shape[0]-y_offset,xcut:l_img.shape[1]-x_offset]
            #l_img[y_offset:y_offset+crop.shape[0], x_offset:x_offset+crop.shape[1]] = crop
            for c in range(0,3):
                l_img[y_offset:y_offset+crop.shape[0], x_offset:x_offset+crop.shape[1], c] = crop[:,:,c] * (crop[:,:,2]/255.0) +  l_img[y_offset:y_offset+crop.shape[0], x_offset:x_offset+crop.shape[1], c] * (1.0 - crop[:,:,2]/255.0)
            # cv2.putText(l_img,"a - Move left",(10,10),FONT_HERSHEY_SIMPLEX,2,(255,255,255),2,cv2.LINE_AA)
            #cv2.imshow('img',l_img)
        _,jpeg=cv2.imencode('.jpg',l_img)    
        return jpeg.tobytes() 
    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


