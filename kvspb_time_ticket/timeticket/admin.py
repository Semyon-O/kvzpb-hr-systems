from django.contrib import admin

from django.contrib import admin
from django.utils.html import format_html

from . import models
from .models import TimeUserWindow


# Register your models here.
@admin.register(models.TimeOrder)
class TimeOrderAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        orders = super().get_queryset(request)
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return orders
            try:
                print(request.user)
                timeOrders = models.TimeOrder.objects.filter(taken_time__user=request.user).all()
                return timeOrders
            except Exception:
                return orders.none()
        return orders.none()

    def get_list_display(self, request):
        return ("person_data", "taken_time", 'id_judgement_place')



@admin.register(models.TimeUserWindow)
class TimeUserWindowAdmin(admin.ModelAdmin):
    fields = ['date',('time_start', 'time_end'), 'status']

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

    def get_list_display(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return ("date", "time_start", "time_end",'status_colored', 'user')

            else:
                return ("date", "time_start", "time_end",'status_colored',)
        return None

    def status_colored(self, obj: TimeUserWindow):
        if obj.status == "open":
            color = "green"
            text = "Запись открыта"
        elif obj.status == "close":
            color = "red"
            text = "Запись закрыта"
        else:
            color = "black"
            text = obj.status

        return format_html(
            f'<span style="border-color:{color}; border-style:solid; border-width: 2px; padding: 3px; border-radius: 30px;">{text}</span>',
        )
    status_colored.short_description = 'Статус'


    def get_queryset(self, request):
        orders = super().get_queryset(request)
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return orders
            try:
                userTimeWindows = models.TimeUserWindow.objects.all().filter(user=request.user)
                return userTimeWindows
            except Exception as e:
                print(e)
                return orders.none()
        return orders.none()