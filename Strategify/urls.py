from django.urls import *
from . import views
from . import kotakservice
from . models import *

urlpatterns = [
    path('', views.home,name="home"),
    path('contactus/', views.contactus,name="contactus"),
    path('aboutus/', views.aboutus,name="aboutus"),
    path('charts/',views.charts,name="charts"),
    path('registration/', views.registration,name="registrationpage"),
    path('profilepage/', views.profilepage,name="profilepage"),
    path('deploypage/', views.deploypage,name="deploypage"),
    path('createstrategy/', views.createstrategy,name="createstrategy"),
    path('creatingStrategy',views.createStrategyForm,name="createsStrategyForm"),
    path('signup/', views.signup, name='signup'),
    path('checking/', views.checkUsername, name='checkUsername'),
    path('signin/', views.signIn, name='signIn'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('generateotp/',views.generateotp, name='generateotp'),
    path('checkstrategyname',views.checkstrategyName,name="checkstrategyname"),
    path('topgainers',views.topgainers,name="topgainers"),
    path('toplosers',views.toplosers,name="toplosers"),
    path('indexdata',views.indexdata,name="indexdata"),
    path('openstrategy',views.openStrategy,name="openStrategy"),
    path('getstockdata',views.stockdata,name="stockdata"),
    path('allindices',views.allindices,name="allindices"),
    path('deletestrategy',views.deletestrategy,name="deletestrategy"),
    path('deploystrategy',views.deploystrategy,name="deploystrategy"),
    path('configure',views.configure,name="configure"),
    path('configurebotdetails/',views.configurebotdetails,name="configurebotdetails"),
    path('savebotdetails/',views.savebotdetails,name="savebotdetails"),
    path('daily_acess_code/',views.daily_acess_code,name="daily_acess_code"),
    path('opensampleStrategy/',views.opensampleStrategy,name="opensampleStrategy"),
    path('webhook/<URL>', views.webhook_call, name='webhook'),
    path('updateProfile',views.updateProfile,name="updateProfile"),
    path('updatePassword',views.updatePassword,name="updatePassword"),

]
