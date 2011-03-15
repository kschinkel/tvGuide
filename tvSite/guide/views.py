import json

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ObjectDoesNotExist
from django.template import Context, loader
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth import logout

from tvSite.guide.models import UserProfile, Show, GuideEntry

from datetime import datetime, time


def get_user_profile(user):
    """
    This function should be used to
    'get or create' a user's profile
    """
    try:
        profile = user.get_profile()
    except ObjectDoesNotExist:
        profile = UserProfile()
        profile.user = request.user
        profile.save()
    return profile


@permission_required('guide.can_have_favs')
def toggleFavShow(request, show_id):
    """
    This function takes a show id as an argument.
    It will toggle a show as a user's favourite
    """
    show_provided = get_object_or_404(Show, id=int(show_id))
    profile = get_user_profile(request.user)
    is_already_fav = profile.fav_shows.filter(id=show_provided.id)
    #If a result was not returned then it was not already a favourite
    if len(is_already_fav) == 0:
        #add the show provided to the user's profile
        profile.fav_shows.add(show_provided)
        return HttpResponse(status=201)
    else:  # The provided show was alread a favourite
        #remove the show provided from the user's profile
        profile.fav_shows.remove(show_provided)
        return HttpResponse()


def logout_user(request):
    """
    This function logs out the user
    then redirects them to the main page
    """
    logout(request)
    return HttpResponseRedirect("/main/")


def tvjson(request, year, month, day):
    """
    This function takes the date provided and returns
    a json object to be displayed in a datatable
    """
    todays_guide = GuideEntry.objects.filter(start__year=year,
                                        start__month=month,
                                        start__day=day)
    shows = []
    for a_entry in todays_guide:
        time = a_entry.start.strftime("%H:%M")
        shows.append([a_entry.show.id, time, a_entry.network,
            a_entry.show.name])

    result = {'aaData': shows}
    return HttpResponse(json.dumps(result), mimetype="application/json")


def favShowList(request):
    """
    This function returns the user's favourites in a json object
    to be displayed in a datatable
    """
    favourites = []
    if request.user.is_authenticated():
        for a_show in get_user_profile(request.user).fav_shows.all():
            favourites.append([a_show.id, a_show.name])

    result = {'aaData': favourites}
    return HttpResponse(json.dumps(result), mimetype="application/json")


def main(request):
    """
    When viewing the main page return the user to the template
    """
    return render_to_response('index.html', {'user': request.user})
