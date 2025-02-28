import asyncio

from django.contrib.auth.models import User
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

from judgment.forms import UploadForm
from judgment.models import Judgment, District

from judgment.services import format_imports

class ImportView(View):

    template_name = 'admin/judgment/judgment/import_judgment_view.html'

    def get(self, request, *args, **kwargs):
        form = UploadForm()
        page = render(request, self.template_name, {'form': form})
        return page


    def post(self, request):
        form = UploadForm(request.POST, request.FILES)

        if form.is_valid():
            file_to_upload = request.FILES['file_to_upload']
            import_context = format_imports.ImportContext(import_format=format_imports.CSVFormatImport())

            data = import_context.import_data_from_file(file_to_upload)
            self.__insert_data_to_models(data)


        return HttpResponse("Succes import")

    def __insert_data_to_models(self, data):
        for judgment in data:
            new_judgment = Judgment()
            new_judgment.id_judgment = judgment["id_judgment"]
            district = District.objects.get_or_create(name=judgment["district"])[0]
            new_judgment.district = district

            new_judgment.fio_judgment = judgment["fio_judgment"]
            new_judgment.phone = judgment["phone"]
            new_judgment.description = judgment["Адрес"]

            inspector = self.__create_or_return_user(judgment['Почта'])
            new_judgment.inspector = inspector

            new_judgment.save()

    def __create_or_return_user(self, email: str):
        user = User.objects.filter(email=email).first()
        if user is None:
            user = User.objects.create_user(email=email, username=email.split('@')[0])
            user.set_password("PassWord@12345")
            user.is_active = False
            user.is_staff = True
            user.save()
            return user
        else:
            return user

