from io import BytesIO
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache
import requests

from app1.models import OtpToken
from app1.models import UserDetails
from .forms import SignUpForm
# from .models import CustomUser
import random
from django.utils import timezone
# Create your views here.

# @login_required(login_url='login')
def home(request):
    return render(request, "index.html")

def loginpage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("user")
        else:
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})
    else:
        return render(request, 'login.html')
    
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.utils import timezone
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data['email']
            gender = form.cleaned_data['gender']
            age = form.cleaned_data['age']
            result = UserDetails(user=user, email=email, gender=gender,age=age)
            result.save()
            # Generate OTP code
            otp_code = get_random_string(length=6, allowed_chars='0123456789')
            # Set OTP expiration time (e.g., 5 minutes from now)
            otp_created_at = timezone.now()

            otp_expires_at = timezone.now() + timezone.timedelta(minutes=5)
            # Save OTP token in the database
            OtpToken.objects.create(user=user, otp_code=otp_code, otp_created_at = otp_created_at, otp_expires_at=otp_expires_at)
            # Send OTP email
            subject = "Email Verification"
            message = render_to_string('otp_email.html', {'otp_code': otp_code})
            sender = "your_email@example.com"  # Update with your sender email address
            receiver = [user.email]
            send_mail(subject, message, sender, receiver)
            # Redirect to the verify-email page
            return redirect('verify_email', username=user.username)
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
         
    # email = request.POST.get('email')
    #         if email:
    #             otp = ''.join(random.choices('0123456789', k=6))
    #             cache.set(email, otp, timeout=300)
    #             send_mail(
    #                 'OTP Verification',
    #                 f'Your OTP is: {otp}',
    #                 settings.EMAIL_HOST_USER,
    #                 [email],
    #                 fail_silently=False,
    #             )
    #             return redirect('verify_email',)
    # else:

# def verify_otp(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         entered_otp = request.POST.get('otp_code')
#         stored_otp = cache.get(email)
#         if stored_otp == entered_otp:
#             cache.delete(email)
#             return redirect('login')
#         else:
#             error_message = 'Invalid OTP. Please try again.'
#             return render(request, 'verify_otp.html', {'email': email, 'error_message': error_message})
#     else:
#         email = request.GET.get('email')
#         return render(request, 'verify_otp.html', {'email': email})

def success(request):
    return render(request, 'success.html')

def logoutuser(request):
    logout(request)
    return redirect('home')


def upload_image(request):
    # Logic for handling the upload image page
    return render(request, 'upload_image.html')  # Assuming 'upload_image.html' is your upload image template


def dashboard(request):
    return render(request, 'dashboards.html')
from django.utils.crypto import get_random_string
from django.utils import timezone
from .models import OtpToken

def verify_email(request, username):
    user = User.objects.get(username=username)
    user_otp = OtpToken.objects.filter(user=user).last()
    
    if request.method == 'POST':
        entered_otp = request.POST.get('otp_code', '')  # Get entered OTP from the form
        stored_otp = user_otp.otp_code  # Get stored OTP from the database
        
        if entered_otp == stored_otp:  # Compare entered and stored OTPs
            if user_otp.otp_expires_at > timezone.now():
                user.is_active = True
                user.save()
                messages.success(request, "Account activated successfully!! You can Login.")
                return redirect('login')
            else:
                messages.warning(request, "The OTP has expired, get a new OTP!")
                return redirect("verify_email", username=user.username)
        else:
            print("User OTP:", user_otp)
            print("Stored OTP:", user_otp.otp_code)
            print("OTP Expiry:", user_otp.otp_expires_at)
            print("Current Time:", timezone.now())
            messages.warning(request, "Invalid OTP entered, enter a valid OTP!")
            return redirect("verify_email", username=user.username)
        
    context = {}
    return render(request, "verify_token.html", context)
 
# def verify_email(request, username):
#     user = User.objects.get(username=username)
#     user_otp = OtpToken.objects.filter(user=user).last()           
    
#     if request.method == 'POST':
#         if user_otp.otp_code == request.POST['otp_code']:
#             if user_otp.otp_expires_at > timezone.now():
#                 user.is_active = True
#                 user.save()
#                 messages.success(request, "Account activated successfully!! You can Login.")


#                 return redirect("signin")
#             else:
#                 messages.warning(request, "The OTP has expired, get a new OTP!")
#                 return redirect("verify_ email", username=user.username)
#         else:
#             print("User OTP:", user_otp)
#             print("Stored OTP:", user_otp.otp_code)
#             print("OTP Expiry:", user_otp.otp_expires_at)
#             print("Current Time:", timezone.now())
#             messages.warning(request, "Invalid OTP entered, enter a valid OTP!")
#             return redirect("verify_email", username=user.username)
         

  
#     context = {}
#     return render(request, "verify_token.html", context)


import os
from django.conf import settings
from django.shortcuts import render
from .models import Predictions


def get_user_images(request):
    # Define the path to the predictions folder
    images = Predictions.objects.all()

    image_urls = {'images':images}

    # Get a list of all image file paths within the predictions folder
    return render(request, 'dashboards.html', image_urls)

def resend_otp(request):
    if request.method == 'POST':
        user_email = request.POST["otp_email"]
        if User.objects.filter(email=user_email).exists():
            user = User.objects.get(email=user_email)
            otp = OtpToken.objects.create(user=user, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))
            subject = "Email Verification"
            message = f"""
                Hi {user.username}, here is your OTP {otp.otp_code} 
                it expires in 5 minute, use the url below to redirect back to the website
                http://127.0.0.1:8000/verify-email/{user.username}
                """
            sender = "clintonmatics@gmail.com"
            receiver = [user.email, ]
            send_mail(
                subject,
                message,
                sender,
                receiver,
                fail_silently=False,
            )
            messages.success(request, "A new OTP has been sent to your email-address")
            return redirect("verify-email", username=user.username)
        else:
            messages.warning(request, "This email doesn't exist in the database")
            return redirect("resend-otp")
    context = {}
    return render(request, "resend_otp.html", context)


def user_home(request):
    data=UserDetails.objects.filter(user=request.user).first()
    return render(request, 'dashboards.html', {'data':data})


def fetch_details(request):
    data = UserDetails.objects.all()  # Fetch all data from the model

    return render(request, 'dashboards.html', {'data': data})

from django.shortcuts import render, HttpResponse
import os

# def handle_upload(request):
#     if request.method == 'POST' and request.FILES.get('fileup'):
#         uploaded_file = request.FILES['fileup']
#         destination_folder = 'D:/VS Code/Aashri\'s Project2/project/save/'

#         try:
#             # Ensure the destination folder exists; create if it doesn't
#             if not os.path.exists(destination_folder):
#                 os.makedirs(destination_folder)

#             # Define the complete path to save the uploaded file
#             destination_path = os.path.join(destination_folder, uploaded_file.name)

#             # Open the destination file in binary write mode and save the uploaded file
#             with open(destination_path, 'wb+') as destination:
#                 for chunk in uploaded_file.chunks():
#                     destination.write(chunk)

#             # Redirect to the same page after successful upload
#             return render(request, 'upload_image.html')

#         except PermissionError as e:
#             return HttpResponse(f"PermissionError: {e}")
#         except Exception as e:
#             return HttpResponse(f"An error occurred: {e}")

#     else:
#         return HttpResponse('Invalid request!')


import os
from PIL import Image
from .models import Predictions
from .forms import ImageUploadForm
import numpy as np
import keras
import tensorflow as tf
from keras.models import load_model

model = load_model('./models/skin_cancer_model.h5')

class_names = {
    0: 'Melanocytic nevi',
    1: 'Melanoma',
    2: 'Benign keratosis-like lesions',
    3: 'Basal cell carcinoma',
    4: 'Actinic keratoses',
    5: 'Basal cell carcinoma',  # Change the name for class index 5
    6: 'Dermatofibroma'
}

def handle_upload(request):
    if request.method == 'POST' and request.FILES.get('fileup'):
        uploaded_file = request.FILES['fileup']
        destination_folder = './save/'

        try:
            # Save the uploaded file to the media folder
            with open(os.path.join(destination_folder, uploaded_file.name), 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # Preprocess the uploaded image
            image = Image.open(uploaded_file)
            processed_image = preprocess_image(image)  # Assuming preprocess_image function exists

            # Make predictions using the loaded model
            prediction, confidence_score = predict_skin_disease(processed_image, model)

            if prediction not in class_names:
                raise Exception("Model is still learning. Unknown class prediction.")
            
            # Get the class name corresponding to the predicted index
            predicted_class_name = class_names[prediction]

            # Save prediction in the database with class name
            prediction_obj = Predictions(user=request.user, image=uploaded_file, prediction=predicted_class_name)
            prediction_obj.save()

            # Redirect to the same page after successful upload
            return render(request, 'upload_image.html', {'prediction': predicted_class_name, 'confidence_score': confidence_score})

        except Exception as e:
            return render(request, 'upload_image.html', {'error': str(e)})

    else:
        form = ImageUploadForm()
        return render(request, 'upload_image.html',{'form':form})

def preprocess_image(image):
    # Resize the image to match the new input shape expected by the model
    resized_image = image.resize((32, 32))  # Resize as needed
    # Convert the image to a numpy array
    img_array = np.array(resized_image)
    # Preprocess the image if needed (e.g., normalize pixel values)
    processed_image = img_array / 255.0  # Normalize pixel values
    # Expand the dimensions to match the input shape expected by the model
    processed_image = np.expand_dims(processed_image, axis=0)
    return processed_image

def predict_skin_disease(processed_image, model):
    try:
        # Make prediction

        prediction = model.predict(processed_image)

        # Get the predicted class index
        predicted_class_idx = np.argmax(prediction)

        # Get the confidence score (optional)
        confidence_score = np.max(prediction)

        return predicted_class_idx, confidence_score

    except Exception as e:
        print(f"Error during prediction: {e}")
        return None, None

def sendmail(request):
    if request.method == "POST":
        feedback = request.POST['feedback']
        email = request.POST['emails']
        

        send_mail(
            'Skinsight Feedback ', #title
           "Feedback --> "+ feedback + "\n"+ 
            "Your feedback has been successfully submitted!! Thank you for commenting on our website" ,#message
            'settings.EMAIL_HOST_USER',
            [email],
            fail_silently=False)

        with open('.\\feedback.txt', 'a') as file:
            file.write(f"Feedback: {feedback}\n")
            file.write(f"Email: {email}\n\n")
        
    return render(request, 'index.html')

def sendmail2(request):
    if request.method == "POST":
        feedback = request.POST['feedback']
        email = request.POST['emails']
        

        send_mail(
            'Skinsight Feedback ', #title
            "Feedback --> "+ feedback + "\n"+ 
            "Your feedback has been successfully submitted!! Thank you for commenting on our website", #message
            'settings.EMAIL_HOST_USER',
            [email],
            fail_silently=False)
        
        with open('.\\feedback.txt', 'a') as file:
            file.write(f"Feedback: {feedback}\n")
            file.write(f"Email: {email}\n\n")
        
    return render(request, 'dashboards.html')
        
