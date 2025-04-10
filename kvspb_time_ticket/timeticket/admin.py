from django.contrib import admin
from django.utils.html import format_html

from . import models
from .models import TimeUserWindow


# Register your models here.
@admin.register(models.TimeOrder)
class TimeOrderAdmin(admin.ModelAdmin):
    raw_id_fields = ("taken_time", )
    search_fields = [
        'person_data__name',  # Поиск по имени кандидата
        'person_data__surname',  # Поиск по фамилии кандидата
        'person_data__email',  # Поиск по email кандидата
    ]

    def get_queryset(self, request):
        orders = super().get_queryset(request)
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return orders
            try:
                if request.user.has_perm('timeticket.can_see_own_record'):
                    timeOrders = models.TimeOrder.objects.filter(taken_time__user=request.user).all()
                    return timeOrders

                if request.user.has_perm('timeticket.view_timeorder'):
                    return orders

            except Exception:
                return orders.none()
        return orders.none()

    def get_list_display(self, request):
        return ("person_data", "taken_time")

@admin.register(models.TimeUserWindow)
class TimeUserWindowAdmin(admin.ModelAdmin):
    fields = ['date',('time_start', 'time_end'), 'status']
    list_filter = ("date", "user__first_name", "status")

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

    def get_list_display(self, request):
        if request.user.is_authenticated:
            return ("date", "time_start", "time_end",'status', 'user__first_name')

        return None

    def get_queryset(self, request):
        orders = super().get_queryset(request)
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return orders
            try:
                if request.user.has_perm('timeticket.can_see_own_record'):
                    userTimeWindows = models.TimeUserWindow.objects.filter(user=request.user).all()
                    return userTimeWindows

                if request.user.has_perm('timeticket.view_timeorder'):
                    return orders
            except Exception as e:
                print(e)
                return orders.none()
        return orders.none()