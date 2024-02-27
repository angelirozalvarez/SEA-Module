from django.contrib import admin
from django.urls import path, include
from trades.views import HomepageView, LandingPageView, signup, loginPage, logoutUser


urlpatterns = [
    path('admin/', admin.site.urls),

    path('home-page/', HomepageView.as_view(), name='home-page'),
    path('', LandingPageView.as_view(), name='landing-page'),

    path('trades/', include('trades.urls'), name='trades'),

    path('signup/', signup, name='signup'),
    path('login/', loginPage, name='login'),
    path('logout/', logoutUser, name='logout')

]
