from django.contrib import admin
from sign.models import Event,Guest
#Register your models here.
class EventAdmin(admin.ModelAdmin):
    list_display = ["id","name1","status1","address1","start_time1"]
    search_fields = ["name1"]
    list_filter = ["status1"]
class GuestAdmin(admin.ModelAdmin):
    list_display = ["realname","phone","email","sign","create_time","event"]
    search_fields = ["realname","phone"]
    list_filter = ["sign"]

admin.site.register(Event,EventAdmin)
admin.site.register(Guest,GuestAdmin)
