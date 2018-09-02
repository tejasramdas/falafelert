from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Reminder
from bs4 import BeautifulSoup
import requests

ven=["The Village","Parkside","EVK"]
mealz=["Breakfast","Brunch","Lunch","Dinner"]

def fetch_list():
	r  = requests.get("https://hospitality.usc.edu/residential-dining-menus/")

	data = r.content
	soup = BeautifulSoup(data, "html.parser")
	#print "done"
	dining = soup.findAll("div", {"class": "dining-location-accordion"})
	day=[0]*12
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


def menu(m,n):
	return day[int(m)*4+int(n)]



def hungry(f):
	opts=[]
	for i in range(3):
		#print ven[i]
		for j in range(4):
			#print mealz[j]
			x=menu(i,j)
			for p in x:
				if f in p:
					opts.append((i,j))
	opts=list(set(opts))
	#for i,j in opts:
		#print mealz[j]+" at "+ven[i]				
	return str(opts)

#hungry("Smoothie")

def run_search(request):
	stuff=fetch_list()
	rem = Reminder.objects.all()
	foodz=Reminder.objects.only("food")
	foodz=list(set(list(foodz)))
	for i in foodz:
		msg=hungry(i)
		for j in rem.filter("food",i).only("phone_number"):
			send_msg(j,msg)

	return HttpResponseRedirect("/")






# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    if request.method=='GET':
    	return render(request, 'index.html')
    if request.method=='POST':
    	rem=Reminder(phone_number=request.POST.get('num'),food=request.POST.get('thing'))
    	rem.save()
    	return HttpResponse("Done")


def db(request):

    reminder = Reminder()
    reminder.save()

    reminders = Reminder.objects.all()

    return render(request, 'db.html', {'reminders': reminders})

