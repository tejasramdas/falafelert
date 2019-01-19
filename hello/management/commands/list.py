
from django.core.management.base import BaseCommand, CommandError
from hello.models import Reminder
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse

class Command(BaseCommand):
	def handle(self, *args, **options):
		rem = Reminder.objects.all().values()
		print(rem)
