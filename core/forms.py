from django import forms
from .models import User


class UserSettingsForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["first_name", "last_name", "profile_picture"]
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "Enter your first name",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "Enter your last name",
                }
            ),
            "profile_picture": forms.ClearableFileInput(
                attrs={
                    "class": "file-input file-input-bordered w-full",
                    "accept": "image/*",
                }
            ),
        }
