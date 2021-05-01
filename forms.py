from .models import Color
from django import forms

class ColorForm(forms.ModelForm):
	class Meta():
		model = Color
		fields = ("grayimg",)
