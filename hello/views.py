from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Reminder
from bs4 import BeautifulSoup
import requests

import urllib.request
import urllib.parse
 
def sendSMS(apikey, numbers, sender, message):
    data =  urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,
        'message' : message, 'sender': sender})
    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.txtlocal.com/send/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    return(fr)



def send_msg(n,m):
	sendSMS('AfekZxO11go-sRgFBDNNLiGHq3HwwEpfYvSZcnFKPR',n,'Popcorn Alerts',m)

ven=["The Village","Parkside","EVK"]
mealz=["Breakfast","Brunch","Lunch","Dinner"]

def fetch_list():
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
	return day	


def menu(day,m,n):
	return day[int(m)*4+int(n)]



def hungry(f,day):
	opts=[]

	for i in range(3):
		#print ven[i]
		for j in range(4):
			#print mealz[j]
			x=menu(day,i,j)
			for p in x:
				if f in p:
					opts.append((i,j))
	opts=list(set(opts))
	res=[]
	for i,j in opts:
		res.append(str(mealz[j]+" at "+ven[i]))
	if len(res)==0:
		return 0			
	return str(res)

#hungry("Smoothie")

def run_search(request):
	stuff=fetch_list()
	rem = Reminder.objects.all()
	foodz=Reminder.objects.only("food").distinct()
	print(foodz)
	foodz=list(set(list(foodz)))
	for i in foodz:
		msg=i.food+" - "+hungry(i.food,stuff)
		if msg!=0:
			for j in rem.filter(food=i.food).only("phone_number"):
				send_msg(j,msg)

	return HttpResponse("Sent Alerts")






# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    if request.method=='GET':
    	return render(request, 'index.html')
    if request.method=='POST':
    	rem=Reminder(phone_number=request.POST.get('num'),food=capitalize(request.POST.get('thing')))
    	rem.save()
    	return HttpResponse("Done")


def db(request):

    reminders = Reminder.objects.all()

    return render(request, 'db.html', {'reminders': reminders})

def dell(request):
	Reminder.objects.all().delete()
	return HttpResponse("deleted")
