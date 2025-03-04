import os

from django import forms


class UploadForm(forms.Form):
    file_to_upload = forms.FileField(widget=forms.FileInput())

    def clean_file_to_upload(self):
        file = self.cleaned_data.get('file_to_upload')

        filename = file.name
        extension = os.path.splitext(filename)[1].lower()

        if extension not in ['.csv', '.xlsx']:
            raise forms.ValidationError("Файл должен быть в формате CSV или XLSX.")

        return file

    def is_valid(self):
        valid = super().is_valid()
        if not valid:
            return False

        try:
            self.clean_file_to_upload()
        except forms.ValidationError as e:
            self.add_error('file_to_upload', e)
            return False

        return True
