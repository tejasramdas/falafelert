from hello.models import Reminder
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
	return sendSMS('AfekZxO11go-sRgFBDNNLiGHq3HwwEpfYvSZcnFKPR',n,'Popcorn Alerts',m)

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
def main():
	stuff=fetch_list()
	rem = Reminder.objects.all()
	sms_res=[]
	for i in rem:
		x=hungry(i.food,stuff)
		msg=str(i.food)+" - "+str(x)
		if x!=0:
			sms_res.append(send_msg(i.phone_number,msg))
	print(sms_res)

if __name__ == '__main__':
 	main() 
 
