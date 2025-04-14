"""
URL configuration for research_showcase project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Import settings and static helper for media file serving during development
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from research.views import search_research  # Import search_research

# Remove the redundant home_view definition here
# def home_view(request):
#     return render(request, "home.html")

urlpatterns = [
    path("admin/", admin.site.urls),
    # Root URL now points to the search/browse view
    path("", search_research, name="home"),  # Changed this line
    # Include research app URLs (submit, review, etc.)
    path("", include("research.urls")),  # Prefix handled in research.urls
    # Include users app URLs (login, logout, profile)
    path("accounts/", include("users.urls")),  # Prefix for user accounts
    # Additional includes or direct paths if needed
]

# Add URL pattern for serving media files during development
if settings.DEBUG:
    urlpatterns += list(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
    # Optionally add static file serving pattern if needed (often handled by runserver automatically)
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom error handlers (optional)
# handler404 = 'your_app.views.view_404'
# handler500 = 'your_app.views.view_500'
