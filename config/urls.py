from django.conf import settings
from django.urls import path, include
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from core.handlers import error400, error403, error404, error500


urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', include('extensions.spectacular')),
    path('accounts/', include('apps.accounts.urls')),
    path('store/', include('apps.store.urls')),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()  # noqa
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # noqa

handler400 = error400
handler400 = error400
handler403 = error403
handler404 = error404
handler500 = error500
