from django.contrib import admin
from django.urls import path, include
from trades.views import HomepageView, landingPage, signupOptionPage, adminSignup, loginPage, logoutUser, regularUserSignup, UnauthorisedMessageView, LogoutConfirmView


urlpatterns = [
    path('admin/', admin.site.urls),

    path('home-page/', HomepageView.as_view(), name='home-page'),
    path('', landingPage, name='landing-page'),
    path('unauthorised-action/', UnauthorisedMessageView.as_view(), name='unauthorised-action'),

    path('trades/', include('trades.urls'), name='trades'),
    path('traders/', include('traders.urls', namespace='traders')),
    path('banks/', include('banks.urls', namespace='banks')),

    path('signup-as/', signupOptionPage, name='signup-option'),
    path('admin-signup/', adminSignup, name='admin-signup'),
    path('user-signup/', regularUserSignup, name='regular-user-signup'),
    path('login/', loginPage, name='login'),
    path('confirm-logout/', LogoutConfirmView.as_view(), name='confirm-logout'),
    path('logout/', logoutUser, name='logout')

]
