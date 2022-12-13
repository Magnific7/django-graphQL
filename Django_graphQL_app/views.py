import re
from django.shortcuts import render, HttpResponse ,HttpResponseRedirect, redirect
from .models import Graph_modal
from django.contrib.auth.models import User
import environ
from decouple import config

def Home(request):
    return render(request, 'index.html', {})

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()

def Index(request):
    context = {}
    error_message = ''
    form = request.POST

    if request.POST:
        try:
            user_id = request.POST['user_id']
            user_name = request.POST['user_name']
            
            user_first_name = request.POST["user_first_name"]

            user_last_name = request.POST["user_last_name"]

            user_email = request.POST['user_email']
            

            user_status = request.POST["user_status"]
            user_phone_number = request.POST['user_phone_number']
            print("user phone",user_phone_number )
            

            Graph_modal.objects.create(user_id=user_id,user_name=user_name,user_first_name=user_first_name,user_last_name=user_last_name,user_email=user_email,user_status=user_status,user_phone_number=user_phone_number)

        except :
            error_message = 'Kindly fill all the form fields '
            context = {}
            return render(request, 'index.html', context)
        
#  text.objects.create(texts=test, upload_text=d)

        error_message = 'Saved to db '

        context = {}
        Graph_modal.objects.create(user_id=user_id,user_name=user_name,user_first_name=user_first_name,user_last_name=user_last_name,user_email=user_email,user_status=user_status,user_phone_number=user_phone_number)

        

        # delete ledger in local storage 
        # if user_name != 'Outward_Cheque':
        
        return render(request, 'index.html', context)


    else:  
        print("no itwems")
        return render(request, 'index.html', context)

def History_page(request):
    history = Graph_modal.objects.all()
    context = {"reports":history} 
    return render(request, 'history.html', context)
    
def Login(request):
    return render(request, 'login.html', {})

def Cancel(request):
    return render(request, 'index.html')
