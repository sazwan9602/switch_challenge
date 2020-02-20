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
	#end update
	#optional function
	#count switch 1
	switch1 = Switch.objects.filter(name='S1')
	switch1_count = Switch.objects.filter(name='S1').count()
	count_sw1_success = 0
	count_sw1_failed = 0
	for cs in switch1.iterator():
		if cs.switch_status == 1:
			count_sw1_success = count_sw1_success + 1
		if cs.switch_status == 0:
			count_sw1_failed = count_sw1_failed + 1

	avg_sw1_success = 0
	avg_sw1_success = count_sw1_success / switch1_count * 100
	avg_sw1_failed = 0
	avg_sw1_failed = count_sw1_failed / switch1_count * 100

	#count switch 2
	switch2 = Switch.objects.filter(name='S2')
	switch2_count = Switch.objects.filter(name='S2').count()
	count_sw2_success = 0
	count_sw2_failed = 0
	for cs in switch2.iterator():
		if cs.switch_status == 1:
			count_sw2_success = count_sw2_success + 1
		if cs.switch_status == 0:
			count_sw2_failed = count_sw2_failed + 1

	avg_sw2_success = 0
	avg_sw2_success = count_sw2_success / switch2_count * 100
	avg_sw2_failed = 0
	avg_sw2_failed = count_sw2_failed / switch2_count * 100

	#count switch 3
	switch3 = Switch.objects.filter(name='S3')
	switch3_count = Switch.objects.filter(name='S3').count()
	count_sw3_success = 0
	count_sw3_failed = 0
	for cs in switch3.iterator():
		if cs.switch_status == 1:
			count_sw3_success = count_sw3_success + 1
		if cs.switch_status == 0:
			count_sw3_failed = count_sw3_failed + 1

	avg_sw3_success = 0
	avg_sw3_success = count_sw3_success / switch3_count * 100
	avg_sw3_failed = 0
	avg_sw3_failed = count_sw3_failed / switch3_count * 100

	contex = {"title":"Home",
			  "count_sw1_success": count_sw1_success, "count_sw1_failed":count_sw1_failed, "avg_sw1_success": round(avg_sw1_success), "avg_sw1_failed": round(avg_sw1_failed),
			  "count_sw2_success": count_sw2_success, "count_sw2_failed":count_sw2_failed, "avg_sw2_success": round(avg_sw2_success), "avg_sw2_failed": round(avg_sw2_failed),
			  "count_sw3_success": count_sw3_success, "count_sw3_failed":count_sw3_failed, "avg_sw3_success": round(avg_sw3_success), "avg_sw3_failed": round(avg_sw3_failed),
			  }

	
	return render(request, 'index.html', contex)

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

