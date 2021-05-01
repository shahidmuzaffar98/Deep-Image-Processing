from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Color
from .forms import ColorForm
import os
from .color_model import colorization
from django.core.files import File
from django.urls import reverse
from django.conf import settings
import requests
import base64
from PIL import Image
from io import BytesIO
# Create your views here.


class ColorListView(LoginRequiredMixin,ListView):
	model = Color
	def get_queryset(self):
		return Color.objects.filter(user=self.request.user)

class ColorDetailView(LoginRequiredMixin,DetailView):
	model = Color

class CreateColorView(LoginRequiredMixin,CreateView):

	form_class = ColorForm

	model = Color

	def get_success_url(self):
		self.object.user = self.request.user
		# if not self.object.clrimg:
		# 	col_img = settings.BASE_DIR + "/" + settings.STATIC_URL + "/" + "8.jpg"
		# 	reopen = open(col_img, "rb")
		# 	django_file = File(reopen)
		# 	self.object.grayimg.save(os.path.basename(col_img), django_file, save=True)

		img_path = self.object.grayimg.url
		img_path = settings.BASE_DIR+"/"+img_path
		with open(img_path, "rb") as image_file:
			encoded_string = base64.b64encode(image_file.read())
		encoded_string = "data:image/png;base64," + encoded_string.decode("utf-8")

		r = requests.post(
			"https://api.deepai.org/api/colorizer",
			data={
				'image': encoded_string,
			},
			headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'}
		)

		out_url = r.json()['output_url']

		response = requests.get(out_url)
		reopen = BytesIO(response.content)
		# reopen = open(gen_img, "rb")
		django_file = File(reopen)

		# os.remove(gen_img)
		self.object.clrimg.save(os.path.basename(img_path), django_file, save=True)

		return reverse("color:detail_c",kwargs={'pk':self.object.id})
