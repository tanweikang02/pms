
from collections import namedtuple
from os import name
from django.urls.conf import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),

    # Authentication
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('create_user', views.create_user, name='create_user'),
    path('change-password/',
         auth_views.PasswordChangeView.as_view(template_name='property/change_password.html', success_url='/profile', extra_context={'edit_profile_success': 'true'})),

    # Property
    path('property/<int:id>', views.property, name='property'),
    path('property/add', views.add_property, name='add_property'),

    # Note
    path('property/<int:id>/create_note',
         views.create_note, name='create_note'),
    path('view_note/<int:id>', views.view_note, name='view_note'),
    path('note', views.note, name='note'),

    # Unit
    path('property/<int:id>/unit/add', views.unit_add, name='unit_add'),
    path('property/<int:id>/unit/add/multiple',
         views.unit_add_multiple, name='unit_add_multiple'),
    path('unit/<int:id>', views.unit, name='unit'),

    # Booking
    path('unit/<int:id>/booking/create',
         views.create_booking, name='create_booking'),
    path('booking', views.booking, name='booking'),
    path('booking/<int:id>', views.view_booking, name='view_booking'),
    path('booking/<int:id>/turn_sale',
         views.turn_booking_to_sale, name='turn_booking_to_sale'),

    # Client
    path('client/<int:id>', views.client, name='client'),

    # Profile
    path('profile', views.profile, name='profile'),

    # Sale
    path('sale', views.sale, name='sale'),
    path('sale/<int:id>', views.view_sale, name='view_sale'),

    ######################

    # API

    #######################


    # Property
    path('api/property/all', views.all_property, name='all_property'),
    path('api/property/<int:id>/units', views.api_units, name='api_units'),
    path('api/property/availability_toggle',
         views.availability_toggle, name='availability_toggle'),

    # Booking Files
    path('api/booking_file/<int:id>',
         views.booking_file_api, name='booking_file_api'),
    path('api/add_booking_file/<int:booking_id>',
         views.add_booking_file, name='add_booking_file'),
    path('api/delete_booking_file/<int:booking_id>',
         views.delete_booking_file, name='delete_booking_file'),

    # Sale Files
    path('api/sale_file/<int:id>',
         views.sale_file_api, name='sale_file_api'),
    path('api/add_sale_file/<int:sale_id>',
         views.add_sale_file, name='add_sale_file'),
    path('api/delete_sale_file/<int:sale_id>',
         views.delete_sale_file, name='delete_sale_file'),


    # Profile
    path('api/edit_profile_data/<str:data>',
         views.edit_data, name='edit_profile_data'),
]
