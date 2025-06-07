from django.contrib import admin
from .models import *

admin.site.register(Thread)
admin.site.register(Message)
admin.site.register(MessageAttachment)
admin.site.register(MessageReceipt)

