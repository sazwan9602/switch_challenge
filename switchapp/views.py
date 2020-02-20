from django.shortcuts import render
from .models import *
import datetime
from django.core.serializers import serialize
import json
from django.db.models.functions import TruncDate

# Create your views here.

def index(request):

	switches = Switch.objects.all()
	#update switch status and created at column 
	if switches.exists():
		for sw in switches.iterator():

			if sw.switch_status is None:
				if(sw.t1==0 and sw.t2==0 and sw.t3==0 and sw.t4==0 and sw.t5==0):
					Switch.objects.filter(pk=sw.id).update(switch_status=0)
				else:
					Switch.objects.filter(pk=sw.id).update(switch_status=1)
			if sw.created_at is None:
				Switch.objects.filter(pk=sw.id).update(created_at=sw.timestamp)
	
	return render(request, 'index.html', {'title':"Home"})

def chart(request):

	select_date = Switch.objects.annotate(date=TruncDate('created_at')).values('date').distinct()

	latest_date_sw1 = Switch.objects.filter(name='S1').latest('id')
	latest_date_sw2 = Switch.objects.filter(name='S2').latest('id')
	latest_date_sw3 = Switch.objects.filter(name='S3').latest('id')
	
	if request.method == 'POST':
		get_date = request.POST.get('dates')
		if(get_date):
			convert_date = datetime.datetime.strptime(get_date, "%Y-%m-%d").date()
			switch1 = Switch.objects.filter(name='S1', created_at__hour__gte=8, created_at__hour__lte=19, created_at__date=convert_date)
			switch2 = Switch.objects.filter(name='S2', created_at__hour__gte=8, created_at__hour__lte=19, created_at__date=convert_date)
			switch3 = Switch.objects.filter(name='S3', created_at__hour__gte=8, created_at__hour__lte=19, created_at__date=convert_date)
			date_preview = convert_date
	else:
		#latest date
		switch1 = Switch.objects.filter(name='S1', created_at__hour__gte=8, created_at__hour__lte=19, created_at__date=latest_date_sw1.created_at)
		switch2 = Switch.objects.filter(name='S2', created_at__hour__gte=8, created_at__hour__lte=19, created_at__date=latest_date_sw2.created_at)
		switch3 = Switch.objects.filter(name='S3', created_at__hour__gte=8, created_at__hour__lte=19, created_at__date=latest_date_sw3.created_at)
		date_preview = latest_date_sw1.created_at.date()

	#convert object to json file
	switch1_json = serialize('json', switch1)
	switch2_json = serialize('json', switch2)
	switch3_json = serialize('json', switch3)

	return render(request, 'chart.html',{"select_date": select_date,
										 "switch_1": switch1_json,
										 "switch_2": switch2_json,
										 "switch_3": switch3_json,
										 "date_sw1": date_preview,})

def alert_report(request):

	switches = Switch.objects.filter(switch_status=0).order_by('-timestamp')


	return render(request, 'alert_report.html', {"switch_var":switches})

