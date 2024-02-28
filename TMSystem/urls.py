from django.contrib import admin
from django.urls import path, include
from trades.views import HomepageView, landingPage, signupOptionPage, adminSignup, loginPage, logoutUser, regularUserSignup, UnauthorisedMessageView


urlpatterns = [
    path('admin/', admin.site.urls),

    path('home-page/', HomepageView.as_view(), name='home-page'),
    path('', landingPage, name='landing-page'),
    path('unauthorised-action/', UnauthorisedMessageView.as_view(), name='unauthorised-action'),

    path('trades/', include('trades.urls'), name='trades'),

    path('signup-as/', signupOptionPage, name='signup-option'),
    path('admin-signup/', adminSignup, name='admin-signup'),
    path('user-signup/', regularUserSignup, name='regular-user-signup'),
    path('login/', loginPage, name='login'),
    path('logout/', logoutUser, name='logout')

]
