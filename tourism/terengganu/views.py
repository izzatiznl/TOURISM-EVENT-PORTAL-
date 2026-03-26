# views.py
from django.shortcuts import render, redirect
from .models import Customer ,Booking ,Package,Review
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse


def homepage(request):
    return render(request, 'homepage.html') 


def packages(request):
    packages = Package.objects.all()  
    return render(request, 'packages.html', {'packages': packages})  

def packages2(request):
    packages = Package.objects.all()  
    return render(request, 'packages2.html', {'packages': packages})  

def homepage2(request):
    return render(request, 'homepage2.html') 

def register(request):
    if request.method == 'POST':
        c_custname= request.POST['custname']
        c_custphone= request.POST['custphone']
        c_custmail= request.POST['custmail']
        c_username= request.POST['username']
        c_password= request.POST['password']

        find_data=Customer.objects.filter(custname=c_custname).values()
          
        if find_data.count()==0:
            data=Customer(custname=c_custname,custphone=c_custphone,custmail=c_custmail,username=c_username,password=c_password)
            data.save()
            dict={
                'message':"Your data has been saved and registered. "
            }
            return redirect('login')
        else:         
            dict={
                    'message':"User " + find_data[0]['custname'] + " already exists"
                } 
    else:
        dict={
            'message':''
        }
    return render (request, "register.html", dict)

    

def login(request):
    if request.method == 'POST':
        name = request.POST['username']
        password = request.POST['password']

        # Filter only from Customer model
        find = Customer.objects.filter(username=name).values()

        if find.exists():
            if find[0]['password'] == password:
                print("login successful!")
                # Save relevant user information in the session
                request.session['user'] = {
                    'custid': find[0]['custid'],
                    'custname': find[0]['custname'],
                    'custmail': find[0]['custmail'],
                    'username': find[0]['username']
                }
                return redirect('profile',custname=find[0]['custname'])  # Redirect to homepage or user profile page
            else:
                context = {"message": "Wrong password"}
                return render(request, 'login.html', context)
        else:
            context = {"message": "Wrong username"}
            return render(request, 'login.html', context)
    else:
        return render(request, 'login.html')



def login_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if 'user' not in request.session:
            return redirect('login')  # Redirect to login if user is not authenticated
        return view_func(request, *args, **kwargs)
    return wrapper_func


@login_required
def profile(request,custname):
    customer1=Customer.objects.get(custname=custname)
    return render(request, 'profile.html', {'customer': customer1})


def logout_view(request):
    # Clear the session data
    if 'user' in request.session:
        del request.session['user']
    return redirect('homepage')  # Redirect to the login page or homepage


def delete_profile(request, custid):
    # Ensure the user is logged in and the session matches the custid being deleted
    if 'user' in request.session and request.session['user']['custid'] == custid:
        data = Customer.objects.get(custid=custid)
        data.delete()
        # Clear the user session after deletion
        del request.session['user']
        return HttpResponseRedirect(reverse('login'))  # Redirect to the login page after deletion
    else:
        return HttpResponseRedirect(reverse('profile'))  # Redirect to the profile page if unauthorized



def update_profile(request, custname):
    print(f"Requested customer name: {custname}")  # Check if custname is received correctly
    try:
        customer = Customer.objects.get(custname=custname)
        print(f"Customer found: {customer}")  # Confirm the customer is found
    except Customer.DoesNotExist:
        print("Customer not found, redirecting to homepage.")
        return redirect('homepage')

    return render(request, 'update_profile.html', {'data': customer})



def save_profile(request,custname):
    if request.method == 'POST':
        s_custname = request.POST['custname']  # Get the customer name from the form
        s_custmail = request.POST['custmail']  # Get the email from the form

        try:
            # Retrieve the Customer object based on the provided name
            customer = Customer.objects.get(custname=custname)

            # Update the customer's details
            customer.custname = s_custname
            customer.custmail = s_custmail
            customer.save()  # Save the changes

            # Redirect to the user profile page or a success page
            return redirect('profile',custname=s_custname)  # Make sure 'profile' is defined in your URLs

        except Customer.DoesNotExist:
            return redirect('homepage') 
            # Handle case where customer does not exist
            
    return update_profile(request, custname)
 

def search(request):
    if request.method == 'GET':
        package_name = request.GET.get("c_packagename")
        
        if package_name:
            data = Package.objects.filter(packagename__icontains=package_name)
        else:
            data = Package.objects.none()  
        dict = {
            'data': data,
        }
        return render(request, 'search.html', dict)
    else:
        return render(request, 'search.html')



def booking(request):
    message = ''
    package = Package.objects.all().values()
    userregister = None

    # Check if the user is logged in
    if 'user' in request.session:
        s_username = request.session['user']['username']  # Fix here
        try:
            user = Customer.objects.get(username=s_username)
        except Customer.DoesNotExist:
            message = "User not found."
            return render(request, 'booking.html', {'message': message, 'package': package})

        # Handle POST request for booking
        if request.method == 'POST':
            s_packageid = request.POST['packagename']
            booking_date = request.POST['bookingdate']
            booking_tickets = request.POST['bookingticket']

            try:
                # Retrieve the Package instance
                c_packageid = Package.objects.get(packageid=s_packageid)
                total_price = c_packageid.packageprice * int(booking_tickets)

                # Create and save a Booking instance
                data = Booking(
                    custid=user,
                    packageid=c_packageid,
                    bookingdate=booking_date,
                    bookingticket=booking_tickets,
                    totalprice=total_price
                )
                data.save()
                message = "Data saved successfully"
                return redirect('display', bookingid=data.bookingid) 

            except Package.DoesNotExist:
                message = "Selected package does not exist."
            except Exception as e:
                message = f"An error occurred: {str(e)}"

        else:
            message = 'Please fill out the booking form.'

    else:
        message = "User not logged in."

    # Render the booking template with the context
    context = {
        'message': message,
        'package': package,
        'userregister': userregister
    }

    return render(request, 'booking.html', context)



def display(request,bookingid=None):
    message=''
    data=None
    if bookingid:
        #retrieve the booking data based on the booking ID
        try:
            data=Booking.objects.get(bookingid=bookingid)
        except Booking.DoesNotExist:
            message="Booking not found."
    
    return render(request, 'display.html',{'data': data, 'message':message})


def delete_booking(request,bookingid):
    data=Booking.objects.get(bookingid=bookingid)
    data.delete()
    return HttpResponseRedirect (reverse('booking'))


def review(request):
    if 'user' in request.session:
        s_username = request.session['user']['username']
        user = Customer.objects.get(username=s_username)

        print("Logged in user:", s_username)  # Debugging statement

        if request.method == 'POST':
            review_comment = request.POST['reviewcomment']
            # Create a review directly associated with the logged-in user
            review = Review(custid=user, reviewcomment=review_comment)
            review.save()
            return redirect('review')

        # Fetch reviews for the logged-in user
        review_user = Review.objects.filter(custid=user)
        print("Reviews for user:", review_user)  # Debugging statement
        return render(request, 'review.html', {'review_user': review_user})

    return redirect('login')


