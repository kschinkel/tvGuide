import json

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import ObjectDoesNotExist
from django.template import Context, loader
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth import logout

from tvSite.guide.models import UserProfile, Show, GuideEntry

from datetime import datetime, time

@permission_required('guide.can_have_favs')
def toggleFavShow(request, show_id):
    """
    Comments for this function
    """
    fav_show = get_object_or_404(Show, id=int(show_id))
    profile = request.user.get_profile()
    is_already_fav = profile.fav_shows.filter(id=fav_show.id)
    if len(is_already_fav) == 0:
        profile.fav_shows.add(fav_show)
        return HttpResponse("ADDED")
    else:
        profile.fav_shows.remove(fav_show)
        return HttpResponse("REMOVED")


def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/main/")


def tvjson(request, year, month, day):
    todays_guide = GuideEntry.objects.filter(start__year=year,
                                        start__month=month,
                                        start__day=day)
    shows = []
    for a_entry in todays_guide:
        time = a_entry.start.strftime("%H:%M")
        shows.append([a_entry.show.id, time, a_entry.network, a_entry.show.name])

    result = {'aaData': shows}
    return HttpResponse(json.dumps(result), mimetype="application/json")


def favShowList(request):
    favourites = []
    if request.user.is_authenticated():
        try:
            profile = request.user.get_profile()
            for a_show in profile.fav_shows.all():
                favourites.append([a_show.id, a_show.name])
        except ObjectDoesNotExist:
            profile = UserProfile()
            profile.user = request.user
            profile.save()
    result = {'aaData': favourites}
    return HttpResponse(json.dumps(result), mimetype="application/json")


def main(request):
    return render_to_response('index.html', {'user': request.user})
