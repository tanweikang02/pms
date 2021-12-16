# Project Overview

This project is a **sale management system** built for property companies. The system only serves 2 target user groups:
 - Property Salespeople: These salespeople use the system to check for available properties and units. And they can book and sell the unit after confirming with clients.
 - System Admins: System admins have all the abilities of the salespeople group. In addition, they can even add properties for sale, toggle properties' availability, create account for salespeople, etc.

# Functionalities Documentation

### User and Authentication

The system allows all users to login, logout, and change their password. Only the superusers (system admins) have the ability to create account for normal user (salespeople). This is a measure for the company to manage the salespeople work under them.

### Note

Users can create an unlimited number of notes for every property. Every note has a title and a body. This function aims to let users put down anything they want.
 - **Note:** show a list of notes the user has made.
 - **View Note:** Clicking any of the notes will bring the user to this page. This page show all the contents of the note.
 - **Create Note:** present a form to let users create notes.

### Property

 - **Property Page:** the page lets users to see all the details of the property including the available units and the notes they have created for the property. To ease the unit introduction process for the salespeople, they are allowed to sort the list of available units by 4 attributes - Price, Number of Floor, Size, or Number of Rooms. Besides, system admins can toggle the availability of properties.

 - **Add Property:** system admins can also add new properties to the system.

### Unit

 - **Unit Page:** the page shows details of units.

 - **Add Unit:** system admins are allowed to add units for properties. To make the process more efficient, users are given two options on adding units.
   1. Add one unit at one time.
   3. Add all units on the same floor at once. 

### Booking

 - **Booking Page:** users can see all the bookings they have made in the format of a list. and clicking any of the bookings will bring them to View Booking Page.
 - **View Booking Page:** all the details for a particular booking will be shown on this page. Only the salesperson who'd made this booking has the ability to view this page. The booking maker can also turn the booking into sale.
 - **Create Booking:** a form is presented to let users create booking.

### Sale

 - **Sale Page and View Sale Page:** very similar to the beforementioned Booking Page and View Booking Page with the exception of the turning-booking-to-sale part.
 - **The Creation of Sales:** there is no 'Create Sale Page' because all sales are created by turning bookings. 

### Client

 - **Client Page:** salespeople can only access the details of clients if she has any business relation with the particular client such as booking and sale. This is a security feature.

### Profile

 - **Profile Page:** Present the personal data and some computed information of the user. Users are allowed and encouraged to edit their personal data to ensure data accuracy. Users can also change password whenever they want.

### Booking and Sale Files

Users are allowed to add and delete any files for the bookings and sales they have created. This provides a way for the salespeople to store and manage any relevant documents, for example, the contracts and important legal documents.

 - **API:** APIs had been created to serve the uploaded files. The files are full of clients' personal data hence they must be well protected. These APIs make sure the files are only accessible for relevant salespeople.
 - **Addition and Deletion:** a few APIs are also created to serve requests related to addition and deletion of files.

## Distinctiveness and Complexity

### Distinctiveness

This project is distinct from all the projects in the CS50W course:

 - **Type:** Unlike other projects, this project is a corporation-system-based project. 
 - **Targeted Users:** It is designed to serve only the employees of a property company and not the public.
 - **Value Creation:** The way this project provides value is distinct. It drives salespeople's efficiency and smoothes business processes.
 - **Importance of Business Logic:** Due to its distinctive use cases, this system's business logic is far more important than other projects. The logic needs to be well-polished and well-programmed to avoid anomalies to the greatest extent.

### Complexity

 - **Complex Logic:** Many logic has to be programmed. One example is "Property units will become unavailable for 7 days when it has been booked. During that period, only 1 possible action can be taken on the unit, which is turning the booking into sale."
 - **Security Measures:** Some necessary security measures have been implemented to prevent the data breach issue. Access will be restricted when a user try to access something they don't have access to. CSRF token is also required when the APIs receive requests from user.
 - **JavaScript:** To make the webpages mobile responsive and enhance user experience, the JavaScript written for this system is more complex than the previous projects. 
 - **Files Uploaded by Users:** It takes quite some time to figure out the best way to let users upload their files to the system. 

# How To Run

1. Optionally create a virtual environment for the project. Make sure Django is installed. If it's not installed, do `pip install django` in the terminal.
2. `cd` into the finalproject directory. To make sure you're in the correct directory, do `dir` if you're using Command Prompt, or `ls` if you're using a Mac. You should be seeing 2 folders (named finalproject and property) and a python file named `manage.py`.
3. Do `python manage.py makemigrations` to make migrations.
4. Do `python manage.py migrate` to apply migrations to the database.
5. Do `python manage.py createsuperuser` to create a super user. This is because users are not allowed to register themselves for the system.
6. Do `python manage.py runserver` to run the server and Voila! You can now start to utilize the system by logging in to the account you had created!
