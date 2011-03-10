from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^admin/', include(admin.site.urls)),
	(r'^main/$', 'tvSite.guide.views.main'),
	(r'^main/tvjson/$', 'tvSite.guide.views.tvjson'),
	(r'^main/toggleFavShow/$', 'tvSite.guide.views.toggleFavShow'),
	(r'^main/favShowList/$', 'tvSite.guide.views.favShowList'),
	(r'^accounts/login/$', "django.contrib.auth.views.login", 
	{"template_name": "login.html"}),
    # Example:
    # (r'^tvSite/', include('tvSite.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
	(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
    {'document_root': '../media', 'show_indexes': True})
)
