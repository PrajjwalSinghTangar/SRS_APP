from django.contrib import admin

from .models import User,Group,Card
# Register your models here.
admin.site.register(User)
admin.site.register(Group)
admin.site.register(Card)