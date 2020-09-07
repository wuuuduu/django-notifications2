import logging

from django.conf import settings
from django.contrib import admin
from django.urls import path, include

logger = logging.getLogger(__name__)

urlpatterns = [
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
