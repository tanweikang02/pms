from django.contrib import admin
from .models import User, Property, Unit, Note

# Register your models here.
admin.site.register(User)
admin.site.register(Property)
admin.site.register(Note)
admin.site.register(Unit)
