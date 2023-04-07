from django.db import models
from django.contrib import admin


class UserRegistration(models.Model):
    username = models.CharField(max_length=100, primary_key=True, blank=False)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=200)
    password = models.CharField(max_length=100)


class UserRegistrationAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'email', 'phone', 'password')


class StrategyRegistration(models.Model):
    strategyid = models.CharField(max_length=100, primary_key=True, blank=False)
    username = models.ForeignKey(UserRegistration, max_length=100, blank=False, on_delete=models.CASCADE)
    strategyname = models.CharField(max_length=100)
    quantity = models.CharField(max_length=100)
    scripname = models.CharField(max_length=100)
    entrycondition = models.CharField(max_length=100)
    stoploss = models.CharField(max_length=100)
    target = models.CharField(max_length=100)
    exitcondition = models.CharField(max_length=100)
    startdate = models.CharField(max_length=100)
    enddate = models.CharField(max_length=100)
    createDate = models.CharField(max_length=50)



class StrategyRegistrationAdmin(admin.ModelAdmin):
    list_display = (
    'strategyid', 'username', 'strategyname', 'quantity', 'scripname', 'entrycondition', 'stoploss', 'target',
    'exitcondition', 'startdate', 'enddate', 'createDate')


class SampleStrategy(models.Model):
    strategyid = models.CharField(max_length=100, primary_key=True, blank=False)
    strategyname = models.CharField(max_length=100)
    quantity = models.CharField(max_length=100)
    scripname = models.CharField(max_length=100)
    entrycondition = models.CharField(max_length=100)
    stoploss = models.CharField(max_length=100)
    target = models.CharField(max_length=100)
    exitcondition = models.CharField(max_length=100)
    startdate = models.CharField(max_length=100)
    enddate = models.CharField(max_length=100)

class SampleStrategyAdmin(admin.ModelAdmin):
    list_display = (
    'strategyid', 'strategyname', 'quantity', 'scripname', 'entrycondition', 'stoploss', 'target',
    'exitcondition', 'startdate', 'enddate')



class Deploy(models.Model):
    deployid = models.CharField(max_length=100, primary_key=True, blank=False)
    strategyid= models.ForeignKey(StrategyRegistration, max_length=100, blank=False, on_delete=models.CASCADE)
    username = models.ForeignKey(UserRegistration, max_length=100, blank=False, on_delete=models.CASCADE)
    scripname = models.CharField(max_length=100)
    deploytime = models.CharField(max_length=100)
    algocycles = models.CharField(max_length=100)

class DeployAdmin(admin.ModelAdmin):
    list_display = ('deployid','strategyid','username','scripname','deploytime','algocycles')


class Configure(models.Model):
    username = models.CharField(max_length=100, primary_key=True, blank=False)
    accesstoken = models.CharField(max_length=200, blank=False)
    userid = models.CharField(max_length=200,blank=False)
    consumerkey = models.CharField(max_length=200,blank=False)
    password = models.CharField(max_length=200,blank=False)
    appid = models.CharField(max_length=200,blank=False)
    accesscode = models.CharField(max_length=200,blank=False)
    url = models.CharField(max_length=300,blank=False)


class ConfigureAdmin(admin.ModelAdmin):
    list_display = ('username', 'accesstoken', 'userid', 'consumerkey', 'password', 'appid','accesscode','url')


class ScripList(models.Model):
    symbol = models.CharField(max_length=100, primary_key=True, blank=False)
    scrip = models.CharField(max_length=400, blank=False)
    instrumenttoken = models.CharField(max_length=200, blank=False)
    index = models.CharField(max_length=200, blank=False)

class ScripListAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'scrip', 'instrumenttoken', 'index')


class Orders(models.Model):
    orderid = models.CharField(max_length=100,primary_key=True,blank=False)
    username = models.ForeignKey(UserRegistration, max_length=100, blank=False, on_delete=models.CASCADE)
    scrip = models.CharField(max_length=100, blank=False)
    price = models.CharField(max_length=200, blank=False)
    date = models.CharField(max_length=200, blank=False)
    time = models.CharField(max_length=200, blank=False)
    transaction_type = models.CharField(max_length=200, blank=False)
    message = models.CharField(max_length=200,blank=False)
    condition = models.CharField(max_length=200,blank=False)


class OrdersAdmin(admin.ModelAdmin):
    list_display = ('orderid', 'username', 'scrip', 'price','date','time','transaction_type','message','condition')


admin.site.register(UserRegistration, UserRegistrationAdmin)
admin.site.register(StrategyRegistration, StrategyRegistrationAdmin)
admin.site.register(SampleStrategy, SampleStrategyAdmin)
admin.site.register(Deploy, DeployAdmin)
admin.site.register(Configure,ConfigureAdmin)
admin.site.register(ScripList,ScripListAdmin)
admin.site.register(Orders,OrdersAdmin)
