from django.shortcuts import render, redirect, HttpResponse,  get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import Project, Upcoming, ProjectImage, UpcomingImage, Appointment, ContactMessage
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
import random
from django.contrib import messages

# Create your views here.
def index(req):
    properties=Project.objects.all()
    up=Upcoming.objects.all()
    context={"properties":properties,"up":up}
    return render(req,"index.html",context)

def about(req):
    return render(req,"about.html")

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone= request.POST.get('phone')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if name and email and subject and message:
            ContactMessage.objects.create(
                name=name,
                phone=phone,
                email=email,
                subject=subject,
                message=message
            )
            send_mail(
                subject=f"New Contact Form Submission: {subject}",
                message=f"From: {name} <{email}>\n\n{message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['mrp93911@gmail.com'],  
                fail_silently=False,
            )

            send_mail(
                subject="Thanks for contacting us!",
                message=f"Hi {name},\n\nThanks for reaching out! We’ve received your message and will get back to you soon.\n\n- LUXEHOMES",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )

            return render(request, 'thank_you.html')
            

    return render(request, 'contact.html')



def thank_you(req):
    return render(req, 'thank_you.html')



def registered(request):
    projects = Project.objects.all()  

    location = request.GET.get('location')
    property_type = request.GET.get('type')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    bhk = request.GET.get('bhk')

    if location:
        projects = projects.filter(area_of_project_located__icontains=location)
    if property_type:
        projects = projects.filter(type_of_project=property_type)
    if min_price:
        projects = projects.filter(price__gte=min_price)
    if max_price:
        projects = projects.filter(price__lte=max_price)
    if bhk:
        projects = projects.filter(no_of_bhk=bhk)
        
    return render(request, "registered.html", {"projects": projects})


def upcoming(request):
    upcoming_projects = Upcoming.objects.all() 
    
    location = request.GET.get('location')
    property_type = request.GET.get('type')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    bhk = request.GET.get('bhk')

    if location:
        upcoming_projects = upcoming_projects.filter(area_of_project_located__icontains=location)
    if property_type:
        upcoming_projects = upcoming_projects.filter(type_of_project=property_type)
    if min_price:
        upcoming_projects = upcoming_projects.filter(price__gte=min_price)
    if max_price:
        upcoming_projects = upcoming_projects.filter(price__lte=max_price)
    if bhk:
        upcoming_projects = upcoming_projects.filter(no_of_bhk=bhk)

    return render(request, "upcoming.html", {"upcoming_projects": upcoming_projects,})


def projectpage(request, project_id):
    project = get_object_or_404(Project, project_id=project_id)
    # Fetch all images related to this project
    project_images = ProjectImage.objects.filter(project=project)
    return render(request, "projectpage.html", {
        "project": project,
        "project_images": project_images
    })

def upcomingdetail(request, upcoming_project_id):
    upcoming = get_object_or_404(Upcoming, upcoming_project_id=upcoming_project_id)
    # Fetch all images related to this upcoming project
    upcoming_images = UpcomingImage.objects.filter(upcoming_project=upcoming)
    return render(request, "upcomingdetail.html", {
        "upcoming": upcoming,
        "upcoming_images": upcoming_images
    })


def generate_time_slots():
    start_time = datetime.strptime('10:00 AM', '%I:%M %p')
    end_time = datetime.strptime('7:00 PM', '%I:%M %p')
    slots = []
    while start_time < end_time:
        slots.append(start_time.strftime('%I:%M %p'))  # Format time as 'HH:MM AM/PM'
        start_time += timedelta(hours=2)  # Increment by 2 hours
    return slots







def book_appointment(req):
    time_slots = generate_time_slots()
    today = datetime.today()

    if req.method == 'POST':
        service_name = req.POST.get('service_name')
        service_description = req.POST.get('service_description')
        service_fee = req.POST.get('service_fee')
        appointment_date = req.POST.get('appointment_date')
        selected_time_slot = req.POST.get('time_slot')

        try:
            appointment_datetime = datetime.strptime(
                f"{appointment_date} {selected_time_slot}", 
                '%Y-%m-%d %I:%M %p'
            )
        except ValueError:
            # Invalid date/time format
            return render(req, 'book_appointment.html', {
                'time_slots': time_slots,
                'today': today,
                'error': "Invalid date or time format. Please try again.",
                'form_data': req.POST
            })

        appointment = Appointment(
            user=req.user,
            service_name=service_name,
            service_description=service_description,
            service_fee=service_fee,
            date=appointment_datetime,
            phone=req.POST.get('phone'),
            email=req.POST.get('email'),
            message=req.POST.get('message', ''),
        )
        appointment.save()
        req.session['appointment_id'] = appointment.id
        return render(req, 'book_success.html')

    return render(req, 'book_appointment.html', {
        'time_slots': time_slots,
        'today': today
    })


def success(request):
    appointment_id = request.session.get('appointment_id')
    appointment = None
    if appointment_id:
        appointment = Appointment.objects.filter(id=appointment_id).first()
    return render(request, 'book_success.html', {'appointment': appointment})



@csrf_exempt
def confirm_appointment(request):
    if request.method == 'POST':
        service_name = request.POST.get('service_name')
        service_description = request.POST.get('service_description')
        service_fee = request.POST.get('service_fee')
        appointment_date = request.POST.get('appointment_date')
        time_slot = request.POST.get('time_slot')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message = request.POST.get('message', '')

        appointment_datetime = datetime.strptime(f"{appointment_date} {time_slot}", '%Y-%m-%d %I:%M %p')

        appointment = Appointment.objects.create(
            user=request.user,
            service_name=service_name,
            service_description=service_description,
            service_fee=service_fee,
            date=appointment_datetime,
            phone=phone,
            email=email,
            message=message,
        )

        request.session['appointment_id'] = appointment.id
        return JsonResponse({'status': 'success'})
    





def user_appointments(req):
    appointments = Appointment.objects.filter(user=req.user) 
    return render(req, 'Appointments.html', {'appointments': appointments})





@login_required
@csrf_exempt
def confirm_appointment(request):
    if request.method == 'POST':
        form_data = request.POST  # or from session if you're storing it there

        appointment_datetime = datetime.strptime(
            f"{form_data['appointment_date']} {form_data['time_slot']}",
            '%Y-%m-%d %I:%M %p'
        )

        Appointment.objects.create(
            user=request.user,
            service_name=form_data['service_name'],
            service_description=form_data['service_description'],
            service_fee=form_data['service_fee'],
            date=appointment_datetime,
            phone=form_data['phone'],
            email=form_data['email'],
            message=form_data['message'],
        )

        # Send Email Confirmation
        send_mail(
            subject='Appointment Confirmation - LUXEHOMES',
            message=f"""Dear {request.user.username},

            Your appointment for "{form_data['service_name']}" has been successfully booked.

            📅 Date: {form_data['appointment_date']}
            ⏰ Time: {form_data['time_slot']}
            📞 Phone: {form_data['phone']}
            📧 Email: {form_data['email']}

            Thank you for choosing LuxeHomes!
            We look forward to seeing you.

            Regards,
            LUXEHOMES Team
            """,
            from_email='your_email@gmail.com',
            recipient_list=[form_data['email']],
            fail_silently=False,
        )

        return JsonResponse({'status': 'success'})








def commercial(req):
    if req.method=="GET":
        allproducts=Upcoming.objects.filter(type_of_project__exact="Commercial")
        print(allproducts)
        context={'allproducts':allproducts}
        return render(req,'upcoming.html',context)
    else:
        allproducts=Project.objects.all()
        print(allproducts)
        context={'allproducts':allproducts}
        return render(req,'upcoming.html',context)

def residential(req):
    if req.method=="GET":
        allproducts=Upcoming.objects.all()
        # allproducts=Product.productmanager.electronics_list()
        allproducts=Upcoming.objects.filter(type_of_project__exact="Residential")
        print(allproducts)
        context={'allproducts':allproducts}
        return render(req,'upcoming.html',context)
    else:
        allproducts=Upcoming.objects.all()
        print(allproducts)
        context={'allproducts':allproducts}
        return render(req,'upcoming.html',context)
































































































































































































def validate_password(password):
    if len(password)<8:
        raise ValidationError("Password must be at least 8 characters long")
    if not any(char.isdigit() for char in password):
        raise ValidationError("Password must contain at least one digit")
    if not any(char.isupper() for char in password):
        raise ValidationError("Password must contain at least one uppercase letter")
    if not any(char.islower() for char in password):
        raise ValidationError("Password must contain at least one lowercase letter")
    if not any(char in ['!','@','#','$','%','^','&','*','(',')'] for char in password):
        raise ValidationError("Password must contain at least one special character")

# signup view to be created
#  signin view to be created 









# def signup(req):
#     print(req.method)
#     context={}
#     if req.method=="GET":
#         return render(req,"signup.html")
#     else:
#         print(req.method)
#         uname=req.POST.get("uname")
#         upass=req.POST.get("upass")
#         ucpass=req.POST.get("ucpass")
#         print(uname,upass,ucpass)
        
#         try:
#             validate_password(upass)
#         except ValidationError as e:
#             context["error"]=str(e)
#             return render(req,"signup.html",context)
        
#         if uname=="" or upass=="" or ucpass=="":
#             context["error"]="All fields are required"
#             return render(req,"signup.html",context)
#         elif upass!=ucpass:
#             context["error"]="Passwords do not match"
#             return render(req,"signup.html",context)
#         elif uname.isdigit():
#             context["error"]="Enter Valid Full Name"
#             return render(req,"signup.html",context)
#         elif upass == uname:
#             context["error"]="Password cannot be same as Username"
#             return render(req,"signup.html",context)
#         else:
#             try:
#                 userdata=User.objects.create(username=uname,password=upass)
#                 userdata.set_password(upass)
#                 userdata.save()
#                 print(User.objects.all())
#                 return redirect("signin")
#             except:
#                 print("User already exists")
#                 context["error"]="Username already exists"
#                 return render(req,"signup.html",context)









def signup(req):
    print(req.method)
    context = {}

    if req.method == "GET":
        return render(req, "signup.html")

    else:
        uname = req.POST.get("uname")
        uemail = req.POST.get("uemail")
        upass = req.POST.get("upass")
        ucpass = req.POST.get("ucpass")

        try:
            validate_password(upass)
        except ValidationError as e:
            context["error"] = str(e)
            return render(req, "signup.html", context)

        if not uname or not uemail or not upass or not ucpass:
            context["error"] = "All fields are required"
            return render(req, "signup.html", context)
        elif upass != ucpass:
            context["error"] = "Passwords do not match"
            return render(req, "signup.html", context)
        elif uname.isdigit():
            context["error"] = "Enter a valid username"
            return render(req, "signup.html", context)
        elif upass == uname:
            context["error"] = "Password cannot be the same as username"
            return render(req, "signup.html", context)
        else:
            try:
                userdata = User.objects.create(username=uname, email=uemail)
                userdata.set_password(upass)
                userdata.save()
                return redirect("signin")
            except:
                context["error"] = "Username already exists"
                return render(req, "signup.html", context)



        
def signin(req):
    if req.method=="POST":
        uname=req.POST.get("uname")
        upass=req.POST.get("upass")
        context={}
        print(uname,upass)
        if uname==""or upass=="":
            context["error"]="All fields are required"
            return render(req,"{% url 'signin' %}",context)
        else:
            userdata=authenticate(username=uname,password=upass)
            if userdata is not None:
                login(req,userdata)
                return redirect("/")
            else:
                context["error"]="Invalid credentials"
                return render(req,"signin.html",context)
    else:
        return render(req,"signin.html")

def userlogout(req):
    logout(req)
    return redirect("/")






def request_password_reset(req):
    if req.method == "POST":
        uname = req.POST.get("uname")

        try:
            user = User.objects.get(username=uname)
            print("User found:", user)

            # Generate OTP and store in session
            userotp = random.randint(100000, 999999)
            req.session["otp"] = userotp
            req.session["uemail"] = user.email  # Save email to session

            # Send OTP via email
            subject = "LUXEHOMES - OTP for Reset Password"
            message = f"""
            Hello {user.username},

            Your OTP to reset your password is: {userotp}

            If you didn’t request this, please ignore this email.

            Thank you,
            LUXEHOMES
            """
            emailfrom = settings.EMAIL_HOST_USER
            receiver = [user.email]
            send_mail(subject, message, emailfrom, receiver)

            return redirect("reset_password")  # Go to next step

        except User.DoesNotExist:
            return render(req, "request_password_reset.html")

    return render(req, "request_password_reset.html")







def reset_password(req):
    # Check if the email is in session (passed from the email reset request form)
    uemail = req.session.get("uemail")
    
    if not uemail:
        # If no email is in session, redirect to the reset form
        return redirect('request_reset_password')

    if req.method == "POST":
        # Get the new password from the form
        new_password = req.POST.get("upass")
        confirm_password = req.POST.get("ucpass")

        if new_password == confirm_password:
            try:
                # Look for the user by email
                user = User.objects.get(email=uemail)
                
                # Set the new password
                user.set_password(new_password)
                user.save()

                # Clear the session data to avoid accidental reuse
                req.session.pop("uemail", None)

                messages.success(req, "Password reset successfully.")
                return redirect('login')  # Redirect to login page after reset

            except User.DoesNotExist:
                messages.error(req, "No user found with that email address.")
        else:
            messages.error(req, "Passwords do not match.")

    return render(req, 'reset_password.html', {
        'email': uemail  # Pass the email to the template for user context
    })