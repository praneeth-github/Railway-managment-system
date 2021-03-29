from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Passenger, Train, Security, Staff
import datetime
import pdfkit
from django.http import HttpResponse
from django.template import loader

# Create your views here.


def login_security(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                if user.user_type == 2:
                    login(request, user)
                    return redirect('security_clearing') #, pk=user.security.id)
                else:
                    return render(request, 'security_login.html', {'error_message': 'Invalid security staff credentials'})
            else:
                return render(request, 'security_login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'security_login.html', {'error_message': 'Invalid login'})
    return render(request, 'security_login.html')


def login_staff(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                if user.user_type == 1:
                    login(request, user)
                    return redirect('staff_home', train_no=user.staff.train_no.train_no)
                else:
                    return render(request, 'staff_login.html', {'error_message': 'Invalid train staff credentials'})
            else:
                return render(request, 'staff_login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'staff_login.html', {'error_message': 'Invalid login'})
    return render(request, 'staff_login.html')


def home(request):
    return render(request, 'home.html')


def clear_security(request):
    data = Passenger.objects.all()
    return render(request, 'security_clearing.html', {'passengers': data})


def clear_for_security(request, pk):
    passenger = get_object_or_404(Passenger, pk=pk)
    passenger.cleared_security_status = request.user.security.id
    passenger.save()

    return redirect('security_clearing')


def staff_home(request, train_no):
    # staff = get_object_or_404(Staff, pk=pk)
    data = Passenger.objects.filter(train_no=train_no)
    return render(request, 'staff_home.html', {'passengers': data, 'train_no': train_no})

    
def view_trains(request):
    data = Train.objects.all()
    return render(request, 'view_trains.html', {'trains': data})


def self_check_in(request, pk):
    passenger = get_object_or_404(Passenger, pk=pk)
    passenger.checked_in_status = True
    passenger.save()
    return redirect('passenger_home', pk=passenger.pk)


def search_by_source(request):
    if request.method == "POST":
        source = request.POST['source']
        if source:
            data = Train.objects.filter(source=source)
            return render(request, 'view_trains.html', {'trains': data})
        else:
            return redirect('view_trains')       
    else:
        return redirect('view_trains')


def search_by_destination(request):
    if request.method == "POST":
        destination = request.POST['destination']
        if destination:
            data = Train.objects.filter(destination=destination)
            return render(request, 'view_trains.html', {'trains': data})
        else:
            return redirect('view_trains')
    else:
        return redirect('view_trains')


def view_available_trains(request):
    if request.method == "POST":
        source = request.POST['source']
        destination = request.POST['destination']
        if source and destination:
            trains = Train.objects.filter(source=source, destination=destination)
            if trains:
                return render(request, 'home.html', {'trains': trains})
            else:
                return render(request, 'home.html', {'error_message_train': "No trains found"})
        else:
            return redirect('home')
    else:
        return redirect('home')


def book_train(request, pk):
    if request.method == "POST":
        train = Train.objects.get(train_no=pk)
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        nationality = request.POST['nationality']
        gender = request.POST['gender']
        dob = request.POST['dob']
        pnr = str(train.train_no) + str(train.destination_code)
        passenger = Passenger(pnr=pnr, first_name=first_name, last_name=last_name, nationality=nationality,
                              train_no=train, gender=gender, dob=dob)
        passenger.save()
        passenger.pnr = str(train.train_no) + str(train.destination_code) + str(passenger.pk)
        passenger.save()
        train.no_of_seats -= 1
        train.save()
        return redirect('passenger_home', pk=passenger.pk)
    else:
        return render(request, 'book_train.html', {'train_no': pk})


def passenger_home(request, pk):
    passenger = Passenger.objects.get(pk=pk)
    return render(request, 'passenger_home.html', {'passenger': passenger})


def view_booking(request):
    if request.method == "POST":  # view existing booking
        pnr = request.POST['pnr']
        try:
            passenger = Passenger.objects.get(pnr=pnr)
        except Passenger.DoesNotExist:
            passenger = None
        if passenger:
            passenger = get_object_or_404(Passenger, pnr=pnr)
            return render(request, 'passenger_home.html', {'passenger': passenger})
        else:
            return render(request, 'home.html', {'error_message_booking': 'No booking found'})



def staff_check_in(request, pk):
    passenger = get_object_or_404(Passenger, pk=pk)
    passenger.checked_in_status = True
    passenger.save()
    return redirect('staff_home', train_no=passenger.train_no.train_no)


def delete_passengers(request, train_no):
    train = Train.objects.get(train_no=train_no)
    passenger = Passenger.objects.filter(train_no=train)
    passenger.delete()
    return redirect('staff_home', train_no=train.train_no)

