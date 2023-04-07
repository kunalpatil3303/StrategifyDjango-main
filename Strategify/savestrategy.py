from .models import *
import datetime

def saveStrategyDetails(response,dataentryCondition,dataexitCondition):
    user = UserRegistration.objects.get(username=response.session['username'])
    StrategyRegistration.objects.create(
        strategyid=response.session['username'] + response.POST.get('strategyname'),
        username=user,
        strategyname=response.POST.get('strategyname'),
        quantity=response.POST.get('quantityLots'),
        scripname=response.POST.get('allscriplist'),
        entrycondition=dataentryCondition,
        stoploss=response.POST.get('stoploss'),
        target=response.POST.get('targetper'),
        exitcondition=dataexitCondition,
        startdate=response.POST.get('startDate'),
        enddate=response.POST.get('stopDate'),
        createDate=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )

