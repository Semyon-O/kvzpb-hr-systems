from django.contrib import admin
from . import forms

from . import models


# Register your models here.
@admin.register(models.TimeOrder)
class TimeOrderAdmin(admin.ModelAdmin):
    raw_id_fields = ("taken_time", )
    search_fields = [
        'person_data__name',  # Поиск по имени кандидата
        'person_data__surname',  # Поиск по фамилии кандидата
        'person_data__email',  # Поиск по email кандидата
    ]
    list_filter = ("taken_time__user__first_name",)

    @admin.display(description="Имя инспектора", ordering="taken_time__user__first_name")
    def taken_time_user_first_name(self, obj):
        return obj.taken_time.user.first_name if obj.taken_time and obj.taken_time.user else None

    def save_model(self, request, obj: models.TimeOrder, form, change):
        obj.taken_time.change_status_to_close()
        return super().save_model(request, obj,form, change)

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
        return ("person_data", "taken_time", 'taken_time_user_first_name')

@admin.register(models.TimeUserWindow)
class TimeUserWindowAdmin(admin.ModelAdmin):
    fields = ['date',('time_start', 'time_end'), 'status']
    list_filter = ("date", "user__first_name","status")
    form = forms.TimeUserWindowForm

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
