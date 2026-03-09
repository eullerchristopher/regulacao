from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

urlpatterns = [
    path('admin/', admin.site.urls),

    # Raiz → redireciona para login
    path('', auth_views.LoginView.as_view(template_name='login.html'), name="login"),

    # Login (opcional, se quiser manter /login/ também)
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name="login_page"),

    # Logout via POST
    path('logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('login')), name="logout"),

    # URLs do app
    path('', include("core.urls")),
]