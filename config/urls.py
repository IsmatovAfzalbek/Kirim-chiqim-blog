
from django.contrib import admin
from django.urls import path, include


from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)




urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/users/", include("apps.app_users.urls")),
    path("api/currencies/", include("apps.app_currencies.urls")),
    path("api/accounts/", include("apps.app_accounts.urls")),
    path("api/categories/", include("apps.app_categories.urls")),
    path("api/transactions/", include("apps.app_transactions.urls")),
    path("api/reports/", include("apps.app_reports.urls")),
    path("api/dashboard/", include("apps.app_dashboard.urls")),
    
    
   
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),

     path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),


]
