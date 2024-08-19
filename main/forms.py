from django import forms
from .models import App
class AppForm(forms.ModelForm):
    class Meta:
        model = App
        exclude = ["uploaded_by"]  
        labels={
            "apk_file_path":"APK File",
        }
        