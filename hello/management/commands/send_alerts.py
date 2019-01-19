from django.core.management.base import BaseCommand, CommandError
from hello.models import Reminder
from bs4 import BeautifulSoup
import requests
import sendgrid
from sendgrid.helpers.mail import *
import urllib.request
import urllib.parse

import os 
class Command(BaseCommand):
	ven=["The Village","Parkside","EVK"]
	mealz=["Breakfast","Brunch","Lunch","Dinner"]
	sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SendGridAPI'))

	def sendSMS(self,apikey, numbers, sender, message):
		data =  urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,
			'message' : message, 'sender': sender})
		data = data.encode('utf-8')
		request = urllib.request.Request("https://api.txtlocal.com/send/?")
		f = urllib.request.urlopen(request, data)
		fr = f.read()
		return(fr)

	def sendEmail(self,ad,bod):
		print(ad)
		from_email = Email("admin@popcornchicken.com")
		to_email = Email(ad)
		subject = bod
		content = Content("text/plain", "YAY")
		mail = Mail(from_email, subject, to_email, content)
		print(mail.get())
		response = self.sg.client.mail.send.post(request_body=mail.get())
		return response.status_code

	def send_msg(self,n,m):
		return self.sendSMS('',n,'Popcorn Alerts',m)


	def fetch_list(self):
		r  = requests.get("https://hospitality.usc.edu/residential-dining-menus/")
		day=[0]*12
		data = r.content
		soup = BeautifulSoup(data, "html.parser")
		#print "done"
		dining = soup.findAll("div", {"class": "dining-location-accordion"})
		for n,meal in enumerate(dining):
			x=meal.findAll("div", {"class": "col-sm-6"})

			for m,i in enumerate(x):
				s=i.findAll("li")
				itemz=[]
				for j in s:
					j.find("span").extract()
					itemz.append(j.text)
				#print (m,n)
				#print itemz
				day[m*4+n]=itemz
		print(day)
		return day  


	def menu(self,day,m,n):
		return day[int(m)*4+int(n)]



	def hungry(self,f,day):
		opts=[]

		for i in range(3):
			#print ven[i]
			for j in range(4):
				#print mealz[j]
				x=self.menu(day,i,j)
				for p in x:
					if f in p and (i,j) not in opts:
						opts.append((i,j))
		#opts=list(set(opts))
		res=[]
		for i,j in opts:
			res.append(str(self.mealz[j]+" at "+self.ven[i]))
		if len(res)==0:
			return 0            
		return str(res)

	#hungry("Smoothie")


	def handle(self, *args, **options):
		stuff=self.fetch_list()
		rem = Reminder.objects.all()
		sms_res=[]
		for i in rem:
			x=self.hungry(i.food,stuff)
			msg=str(i.food)+" - "+str(x)
			if x!=0:
				sms_res.append(self.sendEmail(i.phone_number,msg))
		print(sms_res)


