from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^main/$', 'tvSite.guide.views.main'),
    (r'^main/tvjson/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)$',
        'tvSite.guide.views.tvjson'),
    (r'^logout/$', 'tvSite.guide.views.logout_user'),
    (r'^main/toggleFavShow/(?P<show_id>\d+)$',
        'tvSite.guide.views.toggleFavShow'),
    (r'^main/favShowList/$', 'tvSite.guide.views.favShowList'),
    (r'^accounts/login/$', "django.contrib.auth.views.login",
    {"template_name": "login.html"}),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
    {'document_root': '../media', 'show_indexes': True})
)
