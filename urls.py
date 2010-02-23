from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
	(r'^static/(.*)$', 'django.views.static.serve',
	     {'document_root': settings.MEDIA_ROOT}),
	(r'^i18n/', include('django.conf.urls.i18n')),
)
