from django import forms

class UsersForm(forms.ModelForm):
	class Meta:
		model= Users
		widgets = {
		'password': forms.PasswordInput(),
		}