from django.contrib import admin
from .models import Tags, Authors, Quotes
# Register your models here.
admin.site.register(Tags)
admin.site.register(Authors)
admin.site.register(Quotes)