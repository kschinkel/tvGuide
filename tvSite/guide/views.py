from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
import urllib2
from xml.dom.minidom import parse, parseString
from django.template import Context, loader
from django.contrib.auth.models import User
from tvSite.guide.models import UserProfile
from tvSite.guide.models import Show
from tvSite.guide.models import StartTime
from datetime import datetime, time
import json

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
			rc.append(node.data)
	return ''.join(rc)

@login_required
def toggleFavShow(request):
	if 'showID' not in request.GET:
		return HttpResponse(json.dumps("FAILED"),mimetype="application/json")
	showID = int(request.GET.get("showID"))
	profile = request.user.get_profile()
	fav_show = Show.objects.get(tID=showID)
	for a_fav in profile.fav_shows.all():
		if a_fav == fav_show:
			profile.fav_shows.remove(fav_show)
			return HttpResponse(json.dumps("REMOVED"),mimetype="application/json")
	profile.fav_shows.add(fav_show)
	return HttpResponse(json.dumps("ADDED"),mimetype="application/json")
	
	
@login_required
def tvjson(request):
	if 'year' not in request.GET or 'month' not in request.GET or 'day' not in request.GET:
		return render_to_response('index.html')
	year = request.GET.get("year")
	month = request.GET.get("month")
	day = request.GET.get("day")
	thepage = "unhandled problem"
	
	objList = []
	for a_show in Show.objects.all():
		for shows_today in a_show.start_times.filter(start__year=year, start__month=month, start__day=day):
			time = shows_today.start.strftime("%I:%M%p")
			a_obj = [time,a_show.name,a_show.tID]
			objList.append(a_obj)
			
	dataObj = {'aaData': objList }

	return HttpResponse(json.dumps(dataObj),mimetype="application/json")

@login_required
def favShowList(request):
	fav_list =[]
	try:
		profile = request.user.get_profile()
		for a_show in profile.fav_shows.all():
			fav_list.append(a_show.tID)
	except:		
		profile = UserProfile()
		profile.user = request.user
		profile.save()
		
	#fav_list = ['6318','5714']
	#dataObj = {fav_list }

	return HttpResponse(json.dumps(fav_list),mimetype="application/json")
	
@login_required
def main(request):
	fav_list =[]
	try:
		profile = request.user.get_profile()
		for a_show in profile.fav_shows.all():
			fav_list.append(a_show.tID)
			print "Found fav",a_show.tID
	except:		
		profile = UserProfile()
		profile.user = request.user
		profile.save()
		
	#fav_list = ['6318','5714']
	t = loader.get_template('index.html')
	c = Context( {'user':request.user})

	return HttpResponse(t.render(c))
	#return render_to_response('index.html')