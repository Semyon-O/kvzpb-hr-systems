from django import forms

class UploadForm(forms.Form):
    file_to_upload = forms.FileField(widget=forms.FileInput())