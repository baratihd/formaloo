from django.urls import path, include

from apps.store.views import (
    AppListView,
    AppCreateView,
    PurchaseAppView,
)


urlpatterns = [
    path(
        'apps/',
        include(
            [
                path('', AppListView.as_view(), name='app-list'),
                path('create/', AppCreateView.as_view(), name='app-create'),
                path('<int:app_id>/purchase/', PurchaseAppView.as_view(), name='app-purchase'),
            ]
        ),
    ),
]
