from .savestrategy import *
from django.core.exceptions import *

def updateStrategyData(response,dataentryCondition,dataexitCondition):
    try:
        if StrategyRegistration.objects.filter(username=response.session['username'],strategyid=response.session['username'] + response.POST.get('strategyname')).exists():
            user = UserRegistration.objects.get(username=response.session['username'])
            StrategyRegistration.objects.filter(strategyid = response.session['username'] + response.POST.get('strategyname')).update(
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
                createDate=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                )
        else:
            saveStrategyDetails(response,dataentryCondition,dataexitCondition)
    except ObjectDoesNotExist as e:
        saveStrategyDetails(response,dataentryCondition,dataexitCondition)
