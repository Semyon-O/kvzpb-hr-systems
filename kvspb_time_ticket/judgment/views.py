import os

from django.contrib import messages
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import render
from django.views import View

from judgment.forms import UploadForm
from judgment.models import Judgment, District, Vacancy, VacancyInJudgment

from judgment.services import format_imports

class ImportJudgmentView(View):

    import_template_name = 'admin/judgment/judgment/import_judgment_view.html'

    def get(self, request, *args, **kwargs):
        form = UploadForm()
        page = render(request, self.import_template_name, {'form': form})
        return page

    def post(self, request):
        form = UploadForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                file_to_upload = request.FILES['file_to_upload']
                import_context = format_imports.ImportContext(import_format=format_imports.CSVFormatImport())

                data = import_context.import_data_from_file(file_to_upload)
                self.__insert_data_to_models(data)
                messages.success(request,
                                 'Участки мировых судей успешно импортированы. Можете закрыть данное окно и обновить страницу')
            else:
                messages.error(request,"Произошла ошибка. Данный формат файла нельзя импортировать. Можно импортировать только .xlsx, .csv")
        except KeyError as e:
            print(e)
            messages.error(request, "Импортировать таблицу невозможно. Не соответствие название столбцов. Проверьте пожалуйста наименование столбцов")


        form = UploadForm()
        page = render(request, self.import_template_name, {'form': form})
        return page

    def __insert_data_to_models(self, data):
        for judgment in data:
            new_judgment = Judgment()
            print(judgment)
            new_judgment.id_judgment = judgment["Участок"]
            district = District.objects.get_or_create(name=judgment["Район"])[0]
            new_judgment.district = district

            new_judgment.fio_judgment = judgment["ФИО судьи"]
            new_judgment.phone = judgment["Телефон"]
            new_judgment.description = judgment["Адрес"]

            inspector = self.__create_or_return_user(judgment['Почта'], first_name_inspector=judgment.get("Сотрудник, ответственный за участок"))
            new_judgment.inspector = inspector

            new_judgment.save()

    @staticmethod
    def __create_or_return_user(email: str, *args, **kwargs):
        user = User.objects.filter(email=email).first()
        if user is None:
            user = User.objects.create_user(email=email, username=email.split('@')[0])
            user.first_name = kwargs.get("first_name_inspector", None)
            user.set_password("PassWord@12345")
            user.is_active = False
            user.is_staff = True
            user.save()
            return user
        else:
            return user

class ImportVacanciesInJudgmentView(View):

    import_template_name = 'admin/judgment/vacancyinjudgment/import_vacancy_judgment_view.html'

    def get(self, request, *args, **kwargs):
        form = UploadForm()
        page = render(request, self.import_template_name, {'form': form})
        return page

    def post(self, request):
        form = UploadForm(request.POST, request.FILES)

        try:
            if form.is_valid():
                file_to_upload = request.FILES['file_to_upload']
                extension = os.path.splitext(file_to_upload.name)[1].lower()
                format_contexts = {
                    ".csv": format_imports.CSVFormatImport(),
                    ".xlsx": format_imports.ExcelFormatImport(),
                }
                import_context = format_imports.ImportContext(import_format=format_contexts.get(extension))

                data = import_context.import_data_from_file(file_to_upload)
                self.__insert_data_to_models(data)
                messages.success(request,
                                 "Данные о вакансиях успешно импортированы. Можете закрыть окно и обновить страницу")
            else:
                messages.error(request,"Произошла ошибка. Данный формат файла нельзя импортировать. Можно импортировать только .xlsx, .csv")
        except KeyError:
            messages.error(request, "Произошла ошибка!\n"
                                    "Не соответствие имен столбцов с требуемым форматом. "
                                    "Проверьте чтобы столбец номера участка назывался 'номер участка',"
                                    "и столбец должности назывался 'должность'")
        except IntegrityError as e:
            messages.error(request, f"{e}")


        form = UploadForm()
        page = render(request, self.import_template_name, {'form': form})
        return page

    def __insert_data_to_models(self, data):
        for vacancies_judgment in data:

            vacancy = self.__get_vacancy_object(vacancies_judgment['должность'])
            if vacancy is None:
                raise IntegrityError(f"Данная ванансия не найдена в системе ({vacancies_judgment['должность']}). Проверьте существует ли она?")

            raw_id_judgment = self.__get_judgment_object(vacancies_judgment['номер участка'])

            if not self.__check_existing_vacancies(raw_id_judgment, vacancy):
                VacancyInJudgment.objects.create(
                    judgment=raw_id_judgment,
                    vacancy=vacancy,
                )

    def __check_existing_vacancies(self, id_judgment, vacancy) -> bool:
        is_exist = VacancyInJudgment.objects.filter(
                Q(judgment=id_judgment) &
                Q(vacancy=vacancy)
        ).exists()
        return is_exist

    def __get_judgment_object(self, raw_id_judgment) -> "Judgment":
        judgment_object = Judgment.objects.get(id_judgment=raw_id_judgment)
        return judgment_object

    def __get_vacancy_object(self, raw_name_vacancy) -> "Vacancy":
        position_object = Vacancy.objects.filter(name=raw_name_vacancy).first()
        return position_object