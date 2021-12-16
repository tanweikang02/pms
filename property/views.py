import json
from django.core.paginator import Paginator
from django.db.models.query_utils import Q
from property.models import Booking, BookingFile, Client, Note, Property, Sale, SaleFile, Unit, User
from property.forms import AddPropertyForm, CreateBookingForm, CreateNoteForm, CreateUserForm, EditUserContactForm, EditUserEmailForm, EditUserPasswordForm, EditUserUsernameForm
from django.http.response import FileResponse, HttpResponse, HttpResponseRedirect, JsonResponse
from django.db import IntegrityError
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from datetime import date

from django.conf import settings

# Create your views here.


@login_required(login_url='/login')
def index(request):

    try:
        property_added = request.session['property_added']
    except:
        property_added = 'false'
    request.session['property_added'] = 'false'

    return render(request, 'property/index.html', {
        'property_added': property_added
    })


def login_view(request):

    # GET REQUEST
    if request.method == 'GET':

        try:
            invalid_login = request.session['invalid_login']
        except:
            invalid_login = 'false'
        request.session['invalid_login'] = 'false'

        return render(request, 'property/login.html', {
            'invalid_login': invalid_login
        })

    # POST REQUEST
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect('/')
    request.session['invalid_login'] = 'true'
    return HttpResponseRedirect('/login')


@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required(login_url='/login')
def property(request, id):

    try:
        property = Property.objects.get(id=id)
    except Property.DoesNotExist:
        return render(request, 'property/error.html', {
            'message': 'Property Not Found.',
            'illustration': 'page-not-found'
        })

    try:
        add_unit_success = request.session['add_unit_success']
    except:
        add_unit_success = 'false'
    request.session['add_unit_success'] = 'false'

    try:
        create_note_success = request.session['create_note_success']
    except:
        create_note_success = 'false'
    request.session['create_note_success'] = 'false'

    notes = Note.objects.filter(
        salesperson=request.user, property=property).order_by('-timestamp')

    return render(request, 'property/property.html', {
        'property': property,
        'notes': notes,
        'add_unit_success': add_unit_success,
        'create_note_success': create_note_success
    })


@login_required(login_url='/login')
def create_note(request, id):
    if request.method == 'GET':
        return render(request, 'property/create_note.html')
    form = CreateNoteForm(request.POST)
    if form.is_valid():
        title = form.cleaned_data['title']
        content = form.cleaned_data['content']

        try:
            property = Property.objects.get(id=id)
        except Property.DoesNotExist:
            return render(request, 'property/error.html', {
                'message': 'Property Not Found.',
                'illustration': 'page-not-found'
            })

        Note.objects.create(title=title, content=content,
                            property=property, salesperson=request.user)
        request.session['create_note_success'] = 'true'
        return HttpResponseRedirect(f'/property/{id}')


@login_required(login_url='/login')
def view_note(request, id):
    try:
        note = Note.objects.get(id=id)
    except Note.DoesNotExist:
        return render(request, 'property/error.html', {
            'message': 'Note not found.',
            'illustration': 'page-not-found'
        })
    if note.salesperson != request.user:
        return render(request, 'property/error.html', {
            'message': 'You have no access to this note.',
            'illustration': 'access-denied'
        })
    return render(request, 'property/view_note.html', {
        'note': note
    })


@login_required(login_url='/login')
def note(request):

    notes = Note.objects.filter(
        salesperson=request.user).order_by('-timestamp')

    paginator = Paginator(notes, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    page_obj_number = len(page_obj)

    return render(request, 'property/note.html', {
        'page_obj': page_obj,
        'page_obj_number': page_obj_number
    })


@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def add_property(request):
    if request.method == 'POST':
        form = AddPropertyForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['property_name']
            street = form.cleaned_data['street']
            city = form.cleaned_data['city']
            availability = form.cleaned_data['availability']

            if availability == 'true':
                availability = True
            else:
                availability = False

            Property.objects.create(
                name=name, street=street, city=city, availability=availability)

            request.session['property_added'] = 'true'
            return HttpResponseRedirect('/')
    return render(request, 'property/add_property.html')


@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def create_user(request):
    if request.method == 'GET':
        return render(request, 'property/create_user.html')

    form = CreateUserForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        try:
            user = User.objects.create_user(
                username=username, password=password)
            user.save()
            success = 'true'
        except IntegrityError as e:
            print(e)
            success = 'false'
    else:
        success = 'false'
    return render(request, 'property/create_user.html', {
        'success': success
    })


@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def unit_add(request, id):

    try:
        property = Property.objects.get(id=id)
    except:
        return render(request, 'property/error.html', {
            'message': 'Property Not Found.',
            'illustration': 'page-not-found'
        })

    if request.method == 'POST':
        unit_id = request.POST['unit_id']
        floor = request.POST['floor']
        rooms = request.POST['rooms']
        bathrooms = request.POST['bathrooms']
        size = request.POST['size']
        balcony = request.POST['balcony']
        price = request.POST['price']
        optional_description = request.POST['optional_description']

        if balcony == 'yes':
            balcony = True
        elif balcony == 'no':
            balcony = False

        try:
            unit = Unit(unit_id=unit_id, floor=floor, rooms=rooms, bathrooms=bathrooms,
                        size=size, with_balcony=balcony, price=price, property=property, availability=True,
                        optional_description=optional_description)
            unit.save()
        except:
            request.session['add_unit_error'] = 'true'
            return HttpResponseRedirect(f'/property/{id}/unit/add')

        request.session['add_unit_success'] = 'true'
        return HttpResponseRedirect(f'/property/{id}')

    else:
        try:
            add_unit_error = request.session['add_unit_error']
        except:
            add_unit_error = 'false'
        request.session['add_unit_error'] = 'false'

        try:
            add_multiple_unit_error = request.session['add_multiple_unit_error']
        except:
            add_multiple_unit_error = 'false'
        request.session['add_multiple_unit_error'] = 'false'

        return render(request, 'property/unit_add.html', {
            'property': property,
            'add_multiple_unit_error': add_multiple_unit_error,
            'add_unit_error': add_unit_error
        })


@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def unit_add_multiple(request, id):

    if request.method != 'POST':
        return render(request, 'property/error.html', {
            'message': 'Bad Request.',
            'illustration': 'access-denied'
        })

    try:
        property = Property.objects.get(id=id)
    except:
        return render(request, 'property/error.html', {
            'message': 'Property Not Found.',
            'illustration': 'page-not-found'
        })

    floor = request.POST['floor']
    num_unit = request.POST['num_unit']
    unit_id_start_with = request.POST['unit_id_starts_with']
    description = request.POST['description']

    units = []

    for i in range(1, int(num_unit)+1):
        unit_id = unit_id_start_with + str(i)
        rooms = request.POST[f'rooms-{i}']
        bathrooms = request.POST[f'bathrooms-{i}']
        size = request.POST[f'size-{i}']
        price = request.POST[f'price-{i}']
        balcony = request.POST[f'balcony-{i}']

        if balcony == 'yes':
            balcony = True
        elif balcony == 'no':
            balcony = False

        try:
            units.append(Unit(unit_id=unit_id, floor=floor, rooms=rooms, bathrooms=bathrooms,
                              size=size, with_balcony=balcony, price=price, property=property, availability=True,
                              optional_description=description))
        except:
            request.session['add_multiple_unit_error'] = 'true'
            return HttpResponseRedirect(f'/property/{id}/unit/add')

    # Object creations succeed
    for unit in units:
        unit.save()

    request.session['add_unit_success'] = 'true'
    return HttpResponseRedirect(f'/property/{id}')


@login_required(login_url='/login')
def unit(request, id):

    try:
        unit = Unit.objects.get(id=id)
    except:
        return render(request, 'property/error.html', {
            'message': 'Unit Not Found.',
            'illustration': 'page-not-found'
        })

    try:
        Sale.objects.get(unit=unit)
    except:
        sold_out = False
    else:
        sold_out = True

    # Check If this Unit is within any booking's period currently
    current_booking = None
    booking_end_date = None
    for booking in Booking.objects.filter(unit=unit):
        if booking.date <= date.today() and date.today() < booking.end_date():
            current_booking = booking
            booking_end_date = booking.end_date()
            break

    return render(request, 'property/unit.html', {
        'unit': unit,
        'sold_out': sold_out,
        'current_booking': current_booking,
        'booking_end_date': booking_end_date
    })


@login_required(login_url='/login')
def create_booking(request, id):

    try:
        unit = Unit.objects.get(id=id)
    except:
        return render(request, 'property/error.html', {
            'message': 'Unit Not Found.',
            'illustration': 'page-not-found'
        })

    if request.method == 'POST':
        form = CreateBookingForm(request.POST, request.FILES)
        if form.is_valid():
            customer_name = form.cleaned_data['client_name']
            customer_contact = form.cleaned_data['client_contact']
            customer_email = form.cleaned_data['client_email']
            deposit_amount = form.cleaned_data['deposit']
            files = request.FILES.getlist('files')

            try:
                client = Client.objects.create(
                    name=customer_name, contact=customer_contact, email=customer_email)
            except:
                return render(request, 'property/create_booking.html', {
                    'unit': unit,
                    'customer_creation_error': 'true',
                    'form': form
                })

            try:
                booking = Booking.objects.create(
                    customer=client, salesperson=request.user, unit=unit, deposit=deposit_amount)
            except:
                return render(request, 'property/create_booking.html', {
                    'unit': unit,
                    'booking_creation_error': 'true',
                    'form': form
                })

            for file in files:
                BookingFile.objects.create(booking=booking, file=file)

        return HttpResponseRedirect(f'/booking/{booking.id}')

    else:
        return render(request, 'property/create_booking.html', {
            'unit': unit,
            'form': CreateBookingForm
        })


@login_required(login_url='/login')
def booking(request):

    bookings = Booking.objects.filter(
        salesperson=request.user).order_by('-date')

    paginator = Paginator(bookings, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    page_obj_number = len(page_obj)

    return render(request, 'property/booking.html', {
        'page_obj': page_obj,
        'page_obj_number': page_obj_number
    })


@login_required(login_url='/login')
def view_booking(request, id):

    try:
        booking = Booking.objects.get(id=id)
    except:
        return render(request, 'property/error.html', {
            'message': 'Booking Not Found.',
            'illustration': 'page-not-found'
        })

    try:
        sale_creation_fail = request.session['sale_creation_fail']
    except:
        sale_creation_fail = 'false'
    request.session['sale_creation_fail'] = 'false'

    # Check if the booking has turned into sale
    try:
        Sale.objects.get(booking=booking)
    except:
        turned_to_sale = 'false'
    else:
        turned_to_sale = 'true'

    files = BookingFile.objects.filter(booking=booking)

    if request.user == booking.salesperson:
        return render(request, 'property/view_booking.html', {
            'booking': booking,
            'files': files,
            'number_of_file': files.count(),
            'sale_creation_fail': sale_creation_fail,
            'turned_to_sale': turned_to_sale
        })
    return render(request, 'property/error.html', {
        'message': 'Booking Not Available.',
        'illustration': 'access-denied'
    })


@login_required(login_url='/login')
def client(request, id):

    try:
        client = Client.objects.get(id=id)
    except:
        return render(request, 'property/error.html', {
            'message': 'Client Not Available.',
            'illustration': 'page-not-found'
        })

    bookings = Booking.objects.filter(customer=client)

    for booking in bookings:
        if request.user == booking.salesperson:
            return render(request, 'property/client.html', {
                'client': client
            })

    # The salesperson have no authority to view this client
    return render(request, 'property/error.html', {
        'message': 'Client Not Available.',
        'illustration': 'page-not-found'
    })


@login_required(login_url='/login')
def profile(request):

    try:
        username_taken = request.session['username_taken']
    except:
        username_taken = 'false'
    request.session['username_taken'] = 'false'

    try:
        edit_profile_success = request.session['edit_profile_success']
    except:
        edit_profile_success = 'false'
    request.session['edit_profile_success'] = 'false'

    try:
        same_username_as_before = request.session['same_username_as_before']
    except:
        same_username_as_before = 'false'
    request.session['same_username_as_before'] = 'false'

    try:
        edit_email_fail = request.session['edit_email_fail']
    except:
        edit_email_fail = 'false'
    request.session['edit_email_fail'] = 'false'

    try:
        edit_contact_fail = request.session['edit_contact_fail']
    except:
        edit_contact_fail = 'false'
    request.session['edit_contact_fail'] = 'false'

    return render(request, 'property/profile.html', {
        'num_booking': Booking.objects.filter(salesperson=request.user).count(),
        'num_sale': Sale.objects.filter(salesperson=request.user).count(),
        'num_note': Note.objects.filter(salesperson=request.user).count(),
        'username_taken': username_taken,
        'edit_profile_success': edit_profile_success,
        'same_username_as_before': same_username_as_before,
        'edit_email_fail': edit_email_fail,
        'edit_contact_fail': edit_contact_fail,
    })


@login_required(login_url='/login')
def turn_booking_to_sale(request, id):

    try:
        booking = Booking.objects.get(id=id)
    except:
        return render(request, 'property/error.html', {
            'message': 'Booking Not Available',
            'illustration': 'page-not-found'
        })

    if booking.salesperson != request.user:
        return render(request, 'property/error.html', {
            'message': 'Booking Not Available',
            'illustration': 'page-not-found'
        })

    try:
        sale = Sale.objects.create(customer=booking.customer, unit=booking.unit,
                                   booking=booking, salesperson=request.user)
    except:
        request.session['sale_creation_fail'] = 'true'
        return HttpResponseRedirect(f'/booking/{id}')

    request.session['sale_creation_success'] = 'true'
    return HttpResponseRedirect(f'/sale/{sale.id}')


@login_required(login_url='/login')
def sale(request):

    sales = Sale.objects.filter(
        salesperson=request.user).order_by('-date')

    paginator = Paginator(sales, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    page_obj_number = len(page_obj)

    return render(request, 'property/sale.html', {
        'page_obj': page_obj,
        'page_obj_number': page_obj_number
    })


@login_required(login_url='/login')
def view_sale(request, id):

    try:
        sale = Sale.objects.get(id=id)
    except:
        return render(request, 'property/error.html', {
            'message': 'Sale Not Available.',
            'illustration': 'page-not-found'
        })

    if sale.salesperson != request.user:
        return render(request, 'property/error.html', {
            'message': 'Sale Not Available.',
            'illustration': 'page-not-found'
        })

    files = SaleFile.objects.filter(sale=sale)

    try:
        sale_creation_success = request.session['sale_creation_success']
    except:
        sale_creation_success = 'false'
    request.session['sale_creation_success'] = 'false'

    return render(request, 'property/view_sale.html', {
        'sale': sale,
        'sale_creation_success': sale_creation_success,
        'files': files,
        'number_of_file': files.count(),
    })


##############################################

# API

#############################################

@login_required(login_url='/login')
def all_property(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Bad Request.'}, status=400)
    property = Property.objects.filter(
        availability=True).order_by('-timestamp')
    if property.count() == 0:
        return JsonResponse({'message': 'No Property Available'}, status=400)
    return JsonResponse([item.serialize() for item in property], safe=False)


@login_required(login_url='/login')
def api_units(request, id):
    if request.method != 'GET':
        return JsonResponse({'error': 'Bad Request.'}, status=400)
    try:
        property = Property.objects.get(id=id)
    except Property.DoesNotExist:
        return JsonResponse({'error': 'Property Not Found.'}, status=400)
    units = Unit.objects.filter(property=property)
    return JsonResponse([item.serialize() for item in units], safe=False)


@login_required(login_url='/login')
def availability_toggle(request):
    if request.method != 'PUT':
        return JsonResponse({'error': 'Bad Request.'}, status=400)
    data = json.loads(request.body)
    if data.get("id") is not None:
        try:
            property = Property.objects.get(id=data["id"])
        except Property.DoesNotExist:
            return JsonResponse({'error': 'Property Not Found.'}, status=400)
    if data["availability"] == 'True':
        property.availability = False
    elif data["availability"] == 'False':
        property.availability = True
    property.save()
    return HttpResponse(status=204)


@login_required(login_url='/login')
def booking_file_api(request, id):

    if request.method == 'GET':
        try:
            file = BookingFile.objects.get(id=id)
            print(file)
        except:
            return JsonResponse({'error': 'File Not Available.'}, status=400)
        if file.booking.salesperson == request.user:
            absolute_path = '{}/{}'.format(settings.MEDIA_ROOT, file.file.name)
            return FileResponse(open(absolute_path, 'rb'))
        return JsonResponse({'error': 'File Not Available'}, status=400)
    return JsonResponse({'error': 'Bad Request.'}, status=400)


@login_required(login_url='/login')
def add_booking_file(request, booking_id):

    if request.method == 'POST':
        try:
            booking = Booking.objects.get(id=booking_id)
        except:
            return JsonResponse({'error': 'Booking Not Found'}, status=400)

        files = request.FILES.getlist('files')

        for file in files:
            try:
                BookingFile.objects.create(booking=booking, file=file)
            except:
                return JsonResponse({'error': 'File Addition Failed.'}, status=400)

        return HttpResponseRedirect(f'/booking/{booking_id}')

    return JsonResponse({'error': 'Bad Request.'}, status=400)


@login_required(login_url='/login')
def delete_booking_file(request, booking_id):

    if request.method == 'POST':
        data = json.loads(request.body)

        files_id = data.get('file_id')
        for id in files_id:
            try:
                file = BookingFile.objects.get(id=id)
            except:
                return JsonResponse({'error': 'File Not Found.'}, status=400)

            if file.booking.id == booking_id:
                file.file.delete()
                file.delete()
            else:
                return JsonResponse({'error': 'Deletion Failed'}, status=400)

        return JsonResponse({'message': 'success'}, status=200)

    return JsonResponse({'error': 'Bad Request.'}, status=400)


@login_required(login_url='/login')
def sale_file_api(request, id):

    if request.method == 'GET':
        try:
            file = SaleFile.objects.get(id=id)
            print(file)
        except:
            return JsonResponse({'error': 'File Not Available.'}, status=400)

        if file.sale.salesperson == request.user:
            absolute_path = '{}/{}'.format(settings.MEDIA_ROOT, file.file.name)
            return FileResponse(open(absolute_path, 'rb'))
        return JsonResponse({'error': 'File Not Available'}, status=400)
    return JsonResponse({'error': 'Bad Request.'}, status=400)


@login_required(login_url='/login')
def add_sale_file(request, sale_id):

    if request.method == 'POST':
        try:
            sale = Sale.objects.get(id=sale_id)
        except:
            return JsonResponse({'error': 'Sale Not Found'}, status=400)

        files = request.FILES.getlist('files')

        for file in files:
            try:
                SaleFile.objects.create(sale=sale, file=file)
            except:
                return JsonResponse({'error': 'File Addition Failed.'}, status=400)

        return HttpResponseRedirect(f'/sale/{sale_id}')

    return JsonResponse({'error': 'Bad Request.'}, status=400)


@login_required(login_url='/login')
def delete_sale_file(request, sale_id):

    if request.method == 'POST':
        data = json.loads(request.body)

        files_id = data.get('file_id')
        for id in files_id:
            try:
                file = SaleFile.objects.get(id=id)
            except:
                return JsonResponse({'error': 'File Not Found.'}, status=400)

            if file.sale.id == sale_id:
                file.file.delete()
                file.delete()
            else:
                return JsonResponse({'error': 'Deletion Failed'}, status=400)

        return JsonResponse({'message': 'success'}, status=200)

    return JsonResponse({'error': 'Bad Request.'}, status=400)


@login_required(login_url='/login')
def edit_data(request, data):

    if request.method == 'POST':

        user = request.user

        if data == 'username':
            username = request.POST['username']

            # No changes
            if username == request.user.username:
                request.session['same_username_as_before'] = 'true'

            else:
                form = EditUserUsernameForm(request.POST)

                if form.is_valid():
                    username = form.cleaned_data['username']
                    user.username = username
                    user.save()
                    request.session['edit_profile_success'] = 'true'
                else:
                    request.session['username_taken'] = 'true'

        elif data == 'email':
            form = EditUserEmailForm(request.POST)

            if form.is_valid():
                email = form.cleaned_data['email']
                user.email = email
                user.save()
                request.session['edit_profile_success'] = 'true'
            else:
                request.session['edit_email_fail'] = 'true'

        elif data == 'contact':
            form = EditUserContactForm(request.POST)

            if form.is_valid():
                contact = form.cleaned_data['contact']
                user.contact = contact
                user.save()
                request.session['edit_profile_success'] = 'true'
            else:
                request.session['edit_contact_fail'] = 'true'

        # Eventually all will be directed to profile page
        return HttpResponseRedirect('/profile')

    return JsonResponse({'error': 'Bad Request.'}, status=400)
