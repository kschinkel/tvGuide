from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import ObjectDoesNotExist
from django.template import Context, loader
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, get_list_or_404
from tvSite.guide.models import UserProfile
from tvSite.guide.models import Show
from tvSite.guide.models import StartTime
from datetime import datetime, time
from django.contrib.auth import logout
import json

@login_required
def toggleFavShow(request, show_id):
	if request.user.has_perm('Show.can_have_favs'):
		fav_show = get_object_or_404(Show,id=int(show_id))
		profile = request.user.get_profile()
		for a_fav in profile.fav_shows.all():
			if a_fav == fav_show:
				profile.fav_shows.remove(fav_show)
				return HttpResponse("REMOVED")
		profile.fav_shows.add(fav_show)
		return HttpResponse("ADDED")
	else:
		return HttpResponse("Invalid Permissions!")
	
def logout_user(request):
	logout(request)
	return HttpResponseRedirect("/main/")

def tvjson(request, year, month, day):
	#shows_today = get_list_or_404(Show,start_times__start__year=year, start_times__start__month=month, start_times__start__day=day)
	shows_today = Show.objects.filter(start_times__start__year=year, start_times__start__month=month, start_times__start__day=day)

	shows = []
	for a_show in shows_today:
		for shows_times in a_show.start_times.filter(start__year=year, start__month=month, start__day=day):
			time = shows_times.start.strftime("%I:%M%p")
			shows.append([time, a_show.name, a_show.id])		
	
	result = {'aaData': shows }
	return HttpResponse(json.dumps(result),mimetype="application/json")

def favShowList(request):
	favourites =[]
	if request.user.is_authenticated():
		try:
			profile = request.user.get_profile()
			for a_show in profile.fav_shows.all():
				favourites.append([a_show.name,a_show.id])
		except ObjectDoesNotExist:		
			profile = UserProfile()
			profile.user = request.user
			profile.save()
		
	result = {'aaData' : favourites }
	return HttpResponse(json.dumps(result),mimetype="application/json")
	
def main(request):
	if request.user.is_anonymous():
		welcome_msg = "Hi there! You need to login if you want to add favourites."
		link = '/accounts/login/?next=/main/'
		link_msg = 'Login'
	else:
		welcome_msg = "Welcome, "
		link = '/logout/'
		link_msg = 'Logout'
		if request.user.first_name != "":
			print request.user.first_name
			welcome_msg = welcome_msg + str(request.user.first_name)
		else:
			welcome_msg = welcome_msg + str(request.user.username)
	return render_to_response('index.html', {'welcome_msg' : welcome_msg, 'link' : link, 'link_msg' : link_msg} )