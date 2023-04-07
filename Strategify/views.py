from django.http import JsonResponse
from django.shortcuts import render
from .StockData import *
import pandas as pd
import numpy as np
import yfinance as yf
from .models import *
from datetime import *
from django.core.mail import send_mail
import math, random
from django.core.exceptions import *
from django.db import *
from django.http import HttpResponse
from django.template.loader import render_to_string
from .updatestrategy import *
from .constants import *
from django.contrib import messages
from .backtestprofitlosscalculation import *
from .deploybacktestprofitlosscalculation import *
from .utils import *
from .kotakservice import *
from .yfinance import *
from .orders import *
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

data = None
kotak_bot = None
KOTAK_REQUEST = None
WEBHOOK_URL = None


def home(response):
    return render(response, 'Strategify/index.html', {})


def registration(request):
    return render(request, 'Strategify/registrationPage.html', {})


def aboutus(request):
    return render(request, 'Strategify/aboutus.html', {})

def stockdata(request):
    response_data = {}
    try:
        chartsdata = getScripChartsData(request.POST.get('scripname'), request.POST.get('period'))
        if list(chartsdata.keys())[0] == "error":
            response_data['error'] = str(chartsdata['error'])
        else:
            chartsdata = pd.DataFrame(chartsdata['success'])
            response_data['success'] = chartsdata.values.tolist()
        return JsonResponse(response_data)
    except Exception as e:
        response_data['error'] = str(e)
        print(STOCK_DATA_ERROR, e)
        return JsonResponse(response_data)


def charts(request):
    response_data = {}
    allscrip = []

    userdata = {
        'username': request.session['username'],
        'name': request.session['name'],
        'allscripname': request.session['allscrip'],
    }
    return render(request, 'Strategify/charts.html', {'userdata': userdata, 'status': response_data})


def signup(request):
    response_data = {}
    if request.method == 'POST':
        if request.POST.get('otp') == str(request.session['otp']):
            try:
                UserRegistration.objects.create(
                    username=request.POST.get('username'),
                    name=request.POST.get('name'),
                    email=request.POST.get('email'),
                    phone=request.POST.get('phone'),
                    password=request.POST.get('password'),
                )
                response_data['success'] = ACCOUNT_CREATED
                return JsonResponse(response_data)
            except IntegrityError as e:
                print("Error Account Creating: " + str(e))
                response_data['error'] = ALREADY_ACCOUNT_CREATED
            except Exception as e:
                print("Error Account Creating: " + str(e))
                response_data['error'] = str(e)
                return JsonResponse(response_data)
        else:
            print(INCORRECT_OTP)
            response_data['error'] = INCORRECT_OTP
            return JsonResponse(response_data)
    return JsonResponse(response_data)


def checkUsername(request):
    response_data = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            if UserRegistration.objects.filter(username=username).exists():
                response_data['success'] = AVAILABLE
            else:
                response_data['error'] = NOT_AVAILABLE
        except Exception as e:
            response_data['error'] = str(e)
        return JsonResponse(response_data)


def generateOTP():
    digits = "0123456789"
    OTP = ""
    for i in range(4):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP


def configure(request):
    global kotak_bot,USERNAME, KOTAK_REQUEST
    error = ""
    access = None
    KOTAK_REQUEST = request
    if not request.session['config_status']:
        configstatus = False
        botdata = None
        error = NOT_CONFIGURED
    else:
        configstatus = True
        try:
            botdata = Configure.objects.get(username=request.session['username'])
            kotak = Kotak(botdata.accesstoken,botdata.userid,botdata.consumerkey,botdata.appid,botdata.password)
            kotak.configure()
            kotak.session_login(botdata.accesscode)
            kotak_bot = kotak
            access = True
        except Exception as e:
            access = False
            # if e.reason:
            #     error = str(e.reason)
            print("Kotak Exception: ",e)

    userdata = {
        'username': request.session['username'],
        'name': request.session['name'],
    }

    orderdata = Orders.objects.filter(username=request.session['username']).order_by('-time')[:5]
    data = {
        'isconfigured': configstatus,
        'botdata': botdata,
        'error': error,
        'access':access,
        'orderdata':orderdata,
    }
    print("Kotak Account Configured Status Acess Status: ",access)
    return render(request,'Strategify/configurebot.html',{'userdata':userdata,'data':data})


def configurebotdetails(request):
    response_data = {}
    if request.method == "POST":
        try:
            botdata = Configure.objects.get(username=request.session['username'])
            kotak = Kotak(botdata.accesstoken,botdata.userid,botdata.consumerkey,botdata.appid,botdata.password)
            kotak.configure()
            kotak.session_login(request.POST.get('access_code'))
            response_data['success'] = CONFIGURED_SUCCESS
        except Exception as e:
            if e.reason:
                response_data['error'] = str(e.reason)
            else:
                response_data['error'] = str(e)
            print("Kotak Exception: ", str(e))
    return JsonResponse(response_data)


def daily_acess_code(request):
    response_data = {}
    if request.method == "POST":
        try:
            botdata = Configure.objects.get(username=request.session['username'])
            kotak = Kotak(botdata.accesstoken, botdata.userid, botdata.consumerkey, botdata.appid, botdata.password)
            kotak.configure()
            kotak.session_login(request.POST.get("access_code"))
            Configure.objects.filter(username=request.session['username']).update(
                accesscode = request.POST.get("access_code")
                )
            response_data['success'] = SESSION_LOGGED_IN
        except Exception as e:
            print("Kotak Exception: ", e)
            if e.reason:
                response_data['error'] = str(e.reason)
            else:
                response_data['error'] = str(e)
            
    return JsonResponse(response_data)

def savebotdetails(request):
    response_data = {}
    if request.method == "POST":
        kotak = Kotak(request.POST.get("access_token"), request.POST.get("user_id"),
                      request.POST.get("consumer_key"),
                      "1", request.POST.get("password"))
        try:
            kotak.configure()
            kotak.session_login(request.POST.get("access_code"))
            response_data['success'] = SESSION_LOGGED_IN
            try:
                randomURL = generateRandomURL()
                Configure.objects.create(
                    username=request.session['username'],
                    accesstoken=request.POST.get("access_token"),
                    userid=request.POST.get("user_id"),
                    consumerkey=request.POST.get("consumer_key"),
                    password=request.POST.get("password"),
                    appid="1",
                    accesscode=request.POST.get("access_code"),
                    url="http://127.0.0.1:8000/webhook/"+randomURL,
                )
                request.session['config_status'] = True
                response_data['success'] = REGISTERED_SUCCESS
                response_data['data'] = randomURL
            except IntegrityError as e:
                response_data['error'] = ALREADY_ACCOUNT_CREATED
            except Exception as e:
                response_data['error'] = str(e)
        except Exception as e:
            response_data['error'] = str(e)
            print("Kotak Exception: ", e)
    return JsonResponse(response_data)


@csrf_exempt
@require_POST
def webhook_call(request,URL):
    global kotak_bot,KOTAK_REQUEST
    userdata = UserRegistration.objects.get(username = KOTAK_REQUEST.session['username'])
    botdata = Configure.objects.get(username = KOTAK_REQUEST.session['username'])
    if botdata.url == URL:
        webhook_message = json.loads(request.body)
        if webhook_message['passphrase'] != "aj$Ta786":
            return {
            'code':'error',
            'message': 'nice try buddy'
            }

        price = webhook_message['strategy']['order_price']
        quantity = 1
        symbol = webhook_message['ticker']
        side = webhook_message['strategy']['order_action']

        print("Price: ",price," Symbol: ",symbol," Side: ",side)
        if side == "buy":
            try:
                kotak_bot.place_order("N",symbol,"BUY",quantity,0,0,0,"GFD","REGULAR","STRING")
                saveOrder(generateRandomUID(),userdata,symbol,price,"BUY","Order Placed","success")
                print("BUY Order Placed ! ", symbol, quantity, side)
            except Exception as e:
                print(e)
                saveOrder(generateRandomUID(),userdata,symbol,price,"BUY",str(e.reason),"error")
                print("BUY Exception when calling OrderApi->place_order: %s\n" % e)
        else:
            try:
                kotak_bot.place_order("N",symbol,"SELL",quantity,0,0,0,"GFD","REGULAR","STRING")
                print("SELL Order Placed ! ",symbol, quantity, side)
                saveOrder(generateRandomUID(),userdata,symbol,price,"SELL","Order Placed","success")
            except Exception as e:
                saveOrder(generateRandomUID(),userdata,symbol,price,"SELL",str(e.reason),"error")
                print("SELL Exception when calling OrderApi->place_order: %s\n" % e)
    
    return HttpResponse(status=200)



def generateotp(request):
    response_data = {}
    email = request.POST.get("email")
    try:
        otp = generateOTP()
        request.session['otp'] = otp
        print(otp)
        htmlgen = '<p>Dear Customer, We thank you for registration at Strategify.</p><br><p>Your OTP is <strong>' + otp + '</strong></p>'
        send_mail('OTP request', otp, 'Strategify', [email], fail_silently=False, html_message=htmlgen)
        print("OTP has been SENT")
        response_data['success'] = OTP_SENT
    except Exception as e:
        print("Error OTP sending: " + str(e))
        response_data['error'] = str(e)
        return JsonResponse(response_data)
    return JsonResponse(response_data)


def signIn(request):
    global WEBHOOK_URL
    response_data = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user_data = UserRegistration.objects.get(username=username, password=password)
            if user_data:
                try:
                    data = Configure.objects.get(username=user_data.username)
                    if data.username == user_data.username:
                        request.session['config_status'] = True
                        WEBHOOK_URL = data.url
                except ObjectDoesNotExist as e:
                    print("Config Status: ", str(e))
                    request.session['config_status'] = False
                except Exception as e:
                    print("Config Status: ", str(e))
                    request.session['config_status'] = False
                response_data['success'] = LOGGED_IN
                request.session['username'] = user_data.username
                request.session['name'] = user_data.name
                dashboard(request)
            else:
                response_data['error'] = INVALID_LOGIN
        except ObjectDoesNotExist as e:
            response_data['error'] = INVALID_LOGIN
        except Exception as e:
            response_data['error'] = str(e)
        return JsonResponse(response_data)


def contactus(request):
    return render(request, 'Strategify/contactus.html', {})


def profilepage(request):
    data = UserRegistration.objects.get(username = request.session['username'])
    userdata = {
        'username': request.session['username'],
        'name': request.session['username'],
        'email':data.email,
        'phone':data.phone,
    }
    return render(request, 'Strategify/profilePage.html', {'data': userdata})

def updateProfile(request):
    response_data = {}
    if request.method == "POST":
        try:
            UserRegistration.objects.filter(username = request.session['username']).update(
                name=request.POST.get('name'),
                email = request.POST.get('email'),
                phone = request.POST.get('phone')
                )
            response_data['success'] = "Updated Profile"
        except Exception as e:
            print("Update Profile Error: "+str(e))
            response_data['error'] = "Error Occured"
        return JsonResponse(response_data)

def updatePassword(request):
    response_data = {}
    if request.method == "POST":
        data = UserRegistration.objects.get(username=request.session['username']);
        if request.POST.get("oldpass") == data.password:
            try:
                UserRegistration.objects.filter(username = request.session['username']).update(
                    password = request.POST.get('password')
                    )
                response_data['success'] = "Updated Profile"
            except Exception as e:
                print("Update Password Error: "+str(e))
                response_data['error'] = "Error Occured"
        else:
            response_data['error'] = "Old Password Not Matching"
        return JsonResponse(response_data)

def allindices(request):
    data = UserRegistration.objects.get(username=request.session['username']);
    userdata = {
        'username': request.session['username'],
        'name': data.name,
    }
    return render(request, 'Strategify/allindices.html', {'data': userdata})


def checkstrategyName(request):
    response_data = {}
    if request.method == 'POST':
        try:
            if StrategyRegistration.objects.filter(username=request.session['username'],
                                                   strategyname=request.POST.get('strategyname')).exists():
                response_data['success'] = AVAILABLE
            else:
                response_data['error'] = NOT_AVAILABLE
        except ObjectDoesNotExist as e:
            response_data['success'] = AVAILABLE
        except Exception as e:
            response_data['error'] = str(e)
        return JsonResponse(response_data)


def openStrategy(request):
    response_data = {}
    data = UserRegistration.objects.get(username=request.session['username'])
    strategydata = None
    try:
        if request.method == "GET":
            strategydata = StrategyRegistration.objects.get(strategyid=request.GET.get('strategyid'))
        userdata = {
            'username': request.session['username'],
            'name': request.session['name'],
            'scripdata': request.session['allscrip'],
        }
        return render(request, 'Strategify/createStrategy.html',
                      {'userdata': userdata, 'strategydata': strategydata, 'status': response_data})
    except BrokenPipeError as e:
        print("Connection Error NSE: ", e)
        response_data['error'] = BROKEN_PIPE_ERROR
        return render(request, 'Strategify/createStrategy.html', {'status': response_data})
    except ConnectionError as e:
        print("Connection Error NSE: ", e)
        response_data['error'] = CHECK_CONNECTION
        return render(request, 'Strategify/createStrategy.html', {'status': response_data})
    except Exception as e:
        print("Connection Error NSE: ", e)
        response_data['error'] = str(e)
        return render(request, 'Strategify/createStrategy.html', {'status': response_data})

def opensampleStrategy(request):
    response_data = {}
    data = UserRegistration.objects.get(username=request.session['username'])
    strategydata = None
    try:
        if request.method == "GET":
            strategydata = SampleStrategy.objects.get(strategyid=request.GET.get('strategyid'))
        userdata = {
            'username': request.session['username'],
            'name': request.session['name'],
            'scripdata': request.session['allscrip'],
        }
        return render(request, 'Strategify/createStrategy.html',
                      {'userdata': userdata, 'strategydata': strategydata, 'status': response_data})
    except BrokenPipeError as e:
        print("Connection Error NSE: ", e)
        response_data['error'] = BROKEN_PIPE_ERROR
        return render(request, 'Strategify/createStrategy.html', {'status': response_data})
    except ConnectionError as e:
        print("Connection Error NSE: ", e)
        response_data['error'] = CHECK_CONNECTION
        return render(request, 'Strategify/createStrategy.html', {'status': response_data})
    except Exception as e:
        print("Connection Error NSE: ", e)
        response_data['error'] = str(e)
        return render(request, 'Strategify/createStrategy.html', {'status': response_data})

def deletestrategy(request):
    response_data = {}
    if request.method == "POST":
        try:
            StrategyRegistration.objects.get(
                strategyid=str(request.session['username']) + str(request.POST.get('strategyname'))).delete()
            print("Deleted Sucess")
            return HttpResponse(dashboard(request))
        except ObjectDoesNotExist as e:
            response_data['error'] = str(e)
            rendered = render_to_string('Strategify/error.html', {'error': str(e)})
            return HttpResponse(rendered)
        except Exception as e:
            response_data['error'] = str(e)
            rendered = render_to_string('Strategify/error.html', {'error': str(e)})
            return HttpResponse(rendered)


def createstrategy(request):
    print(request)
    data = UserRegistration.objects.get(username=request.session['username'])
    userdata = {
        'username': request.session['username'],
        'name': request.session['name'],
        'scripdata': request.session['allscrip'],
    }
    return render(request, 'Strategify/createStrategy.html', {'userdata': userdata, 'strategydata': None})


def deploystrategy(request):
    response_data = {}
    scriplist = request.POST.get('allscriplist').split("/")
    strategyname = scriplist[0]
    scriplist = scriplist[:-1]
    strategyid = StrategyRegistration.objects.get(strategyid=request.session['username'] + strategyname)
    user = UserRegistration.objects.get(username=request.session['username'])

    for i in range(1, len(scriplist)):
        try:
            Deploy.objects.create(
                deployid=request.session['username'] + "/" + strategyname + "/" + scriplist[i],
                strategyid=strategyid,
                username=user,
                scripname=scriplist[i],
                deploytime=date.today().strftime('%Y-%m-%d'),
                algocycles=request.POST.get('algocycles'),
            )
            response_data['success'] = DEPLOYED_SUCCESS
        except Exception as e:
            print("Depoy Error: ",str(e))
            response_data['error'] = ERROR_OCCURRED
    return JsonResponse(response_data)


def deploypage(request):
    global data
    userdatainfo = UserRegistration.objects.get(username=request.session['username'])
    userdata = {
        'username': request.session['username'],
        'name': request.session['name'],
    }
    alldata = []
    deployedstrategy = Deploy.objects.filter(username = request.session['username'])
    for i in deployedstrategy:
        deploystrategydata = StrategyRegistration.objects.get(strategyid=i.strategyid.strategyid)
        entryCondition = str(deploystrategydata.entrycondition).split("/")
        exitCondition = deploystrategydata.exitcondition.split("/")
        days = 0
        try:
            days = extractMaximum(deploystrategydata.entrycondition)
            startDate = subtarctdays(i.deploytime, days)
            stopDate = date.today().strftime('%Y-%m-%d')

            try:
                print("Scrip Name: ",i.scripname)
                data = getScripData(i.scripname,startDate,stopDate)
                data['Position'] = None
            except ConnectionError as e:
                print("Error Fetch Stock Data: ", e)

            for k in range(len(entryCondition)-1):
                a = entryCondition[k].split("-")[0].split(",")
                b = entryCondition[k].split("-")[1].split(",")
                c = entryCondition[k].split("-")[2]
                x = b[0]
                b[0] = a[1]
                a[1] = x

                globals()[a[0]]("ENTRY", int(b[0]))
                globals()[a[1]]("ENTRY", int(b[1]))
                entrySignalGeneration(str(a[0]) + str(b[0]), str(a[1]) + str(b[1]),str(c))
            if exitCondition[0] != "None":
                for k in range(len(exitCondition)-1):
                    a = exitCondition[k].split("-")[0].split(",")
                    b = exitCondition[k].split("-")[1].split(",")
                    x = b[0]
                    b[0] = a[1]
                    a[1] = x

                    globals()[a[0]]("EXIT", int(b[0]))
                    globals()[a[1]]("EXIT", int(b[1]))
                    exitSignalGeneration(str(a[0]) + str(b[0]), str(a[1]) + str(b[1]),str(c))


            deploystrategyprevdaysremoval(i.deploytime)
            if exitCondition[0] != "None":

                val = deployprofitLossCalculationWithExit(data, deploystrategydata.strategyname, i.scripname,
                                                    deploystrategydata.target,
                                                    deploystrategydata.stoploss,
                                                    deploystrategydata.quantity,i.algocycles,i.deploytime)
            else:
                val = deployprofitLossCalculationWithoutExit(data, deploystrategydata.strategyname, i.scripname,
                                                       deploystrategydata.target,
                                                       deploystrategydata.stoploss,
                                                       deploystrategydata.quantity,i.algocycles, i.deploytime)
            alldata.append(val)

        except Exception as e:
            print("Error", e)

    return render(request, 'Strategify/deployed.html', {'userdata': userdata,'deploydata':alldata})


def topgainers(request):
    response_data = {}
    try:
        nse = NSE()
        response_data['success'] = nse.topgainers()
        return JsonResponse(response_data)
    except ConnectionError as e:
        response_data['error'] = FAILED_TO_LOAD
        print("Connection Error: ", e)
        return JsonResponse(response_data)
    except Exception as e:
        print("Top Gainers Error: ", str(e))
        response_data['error'] = FAILED_TO_LOAD
        return JsonResponse(response_data)


def toplosers(request):
    response_data = {}
    try:
        nse = NSE()
        response_data['success'] = nse.toplosers()
        return JsonResponse(response_data)
    except ConnectionError as e:
        response_data['error'] = FAILED_TO_LOAD
        print("Connection Error: ", e)
        return JsonResponse(response_data)
    except Exception as e:
        print("Top Losers Error: ", str(e))
        response_data['error'] = FAILED_TO_LOAD
        return JsonResponse(response_data)


def indexdata(request):
    response_data = {}
    try:
        nse = NSE()
        response_data['success'] = nse.allindex()
        return JsonResponse(response_data)
    except ConnectionError as e:
        print("Connection Error: ", e)
    except Exception as e:
        print("Top Losers Error: ", str(e))
        response_data['error'] = str(e)
    return JsonResponse(response_data)


def dashboard(request):
    userdata = {
        'username': request.session['username'],
        'name': request.session['name'],
    }

    allstrategydata  =  []
    samplestrategy = []

    for i in showStrategyDetails(request):
        current = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ends = datetime.strptime(i.createDate, '%Y-%m-%d %H:%M:%S')
        start = datetime.strptime(current, '%Y-%m-%d %H:%M:%S')
        strategydata = {
            'strategyname': i.strategyname,
            'quantity': i.quantity,
            'scripname': i.scripname,
            'entrycondition': i.entrycondition,
            'stoploss': i.stoploss,
            'target': i.target,
            'exitcondition': i.exitcondition,
            'startdate': i.startdate,
            'enddate': i.enddate,
            'createDate': convertTime(start - ends),
        }
        allstrategydata.append(strategydata)

    for i in showSampleStrategy(request):
        samplestrategydata = {
            'strategyname': i.strategyname,
            'quantity': i.quantity,
            'scripname': i.scripname,
            'entrycondition': i.entrycondition,
            'stoploss': i.stoploss,
            'target': i.target,
            'exitcondition': i.exitcondition,
            'startdate': i.startdate,
            'enddate': i.enddate,
        }
        samplestrategy.append(samplestrategydata)
        allscrip = []
        scrip = ScripList.objects.all()
        for i in scrip:
            allscrip.append(i.symbol)
        request.session['allscrip'] = allscrip
    return render(request, 'Strategify/dashboard.html', {'userdata': userdata, 'strategydata': allstrategydata,'sampleStrategy':samplestrategy})


def showStrategyDetails(response):
    data = StrategyRegistration.objects.filter(username=response.session['username'])
    return data

def showSampleStrategy(request):
    data = SampleStrategy.objects.all()
    return data


def createStrategyForm(response):
    global data
    entryCondition = []
    exitCondition = []
    response_data = {}
    dataentryCondition = ""
    dataexitCondition = ""
    try:
        if response.method == "POST":
            j = 1
            for i in response.POST:
                tempCondition = []
                a = response.POST.get("entryfirindicator" + str(j))
                b = response.POST.get("entrysecindicator" + str(j))
                c = response.POST.get("entrycomparator" + str(j))

                if ((a and b and c) != None):
                    tempCondition.append(a)
                    tempCondition.append(c)
                    tempCondition.append(b)
                    entryCondition.append(tempCondition)
                    dataentryCondition += str(a) + "-" + str(b) + "-" + str(c) + "/"
                j += 1
            j = 1
            for i in response.POST:
                tempCondition = []
                a = response.POST.get("exitfirindicator" + str(j))
                b = response.POST.get("exitsecindicator" + str(j))
                c = response.POST.get("exitcomparator" + str(j))

                if ((a and b and c) != None):
                    tempCondition.append(a)
                    tempCondition.append(c)
                    tempCondition.append(b)
                    exitCondition.append(tempCondition)
                    dataexitCondition += str(a) + "-" + str(b) + "-" + str(c) + "/"
                j += 1

            startDate = response.POST.get('startDate')
            stopDate = response.POST.get('stopDate')
            scriplist = response.POST.get('allscriplist')
            scriplist = scriplist.split(",")
            alldata = []
            for i in range(0, len(scriplist) - 1):
                try:
                    data = getScripData(scriplist[i],startDate,stopDate)
                    data['Position'] = None
                except ConnectionError as e:
                    print(e)

                for k in range(len(entryCondition)):
                    a = entryCondition[k][0].split(",")
                    b = entryCondition[k][2].split(",")
                    c = entryCondition[k][1]
                    x = b[0]
                    b[0] = a[1]
                    a[1] = x

                    globals()[a[0]]("ENTRY", int(b[0]))
                    globals()[a[1]]("ENTRY", int(b[1]))
                    entrySignalGeneration(str(a[0]) + str(b[0]), str(a[1]) + str(b[1]),str(c))

                if exitCondition:
                    for k in range(len(exitCondition)):
                        a = exitCondition[k][0].split(",")
                        b = exitCondition[k][2].split(",")
                        c = exitCondition[k][1]
                        print("Exit: ",c)
                        x = b[0]
                        b[0] = a[1]
                        a[1] = x
                        globals()[a[0]]("EXIT", int(b[0]))
                        globals()[a[1]]("EXIT", int(b[1]))
                        exitSignalGeneration(str(a[0]) + str(b[0]), str(a[1]) + str(b[1]),str(c))

                if exitCondition:
                    val = ProfitLossCalculationWithExit(data, response.session['username'], scriplist[i],
                                                        response.POST.get('targetper'), response.POST.get('stoploss'),
                                                        response.POST.get('quantityLots'))
                else:
                    val = ProfitLossCalculationWithoutExit(data, response.session['username'], scriplist[i],
                                                           response.POST.get('targetper'),
                                                           response.POST.get('stoploss'),
                                                           response.POST.get('quantityLots'))
                alldata.append(val)

            if dataexitCondition == "":
                dataexitCondition = "None"
            try:
                updateStrategyData(response, dataentryCondition, dataexitCondition)
            except IntegrityError as e:
                response_data['error'] = STRATEGY_ALREADY_EXIT
            except Exception as e:
                response_data['error'] = str(e)
            return render(response, 'Strategify/backtestHistory.html',
                          {'name':response.session['username'],  'response': response, 'data': alldata, 'strategyName': response.POST.get('strategyname'),
                           'error': response_data})
    except Exception as e:
        print("Error", e)


def Value(condition, period):
    global data
    data['{}Value{}'.format(condition, period)] = period


def Close(condition, period):
    global data
    data['{}Close{}'.format(condition, period)] = data['Close']


def MA(condition, period):
    global data
    try:
        data['{}MA{}'.format(condition, period)] = data['Close'].rolling(window=period).mean()
    except Exception as e:
        print("Error MA: ", e)


def EMA(condition, days):
    global data
    data['{}EMA{}'.format(condition, days)] = data['Close'].ewm(span=days, adjust=False).mean()


def WMA(condition, period):
    global data
    weights = np.arange(1, period + 1)
    wmas = data['Close'].rolling(period).apply(lambda x: np.dot(x, weights) / weights.sum(), raw=True).to_list()
    data['{}WMA{}'.format(condition, period)] = wmas


def RSI(condition, period):
    ret = data['Close'].diff()
    up = []
    down = []
    for i in range(len(ret)):
        if ret[i] < 0:
            up.append(0)
            down.append(ret[i])
        else:
            up.append(ret[i])
            down.append(0)
    up_series = pd.Series(up)
    down_series = pd.Series(down).abs()
    up_ewm = up_series.ewm(com=period - 1, adjust=False).mean()
    down_ewm = down_series.ewm(com=period - 1, adjust=False).mean()
    rs = up_ewm / down_ewm
    rsi = 100 - (100 / (1 + rs))
    rsi_df = pd.DataFrame(rsi).rename(columns={0: 'rsi'}).set_index(data['Close'].index)
    rsi_df = rsi_df.dropna()
    data['{}RSI{}'.format(condition, period)] = rsi_df[3:]


def entrySignalGeneration(period1, period2, operator):
    global data
    if operator == "0":
        data['EntrySignal'] = np.where(data['ENTRY{}'.format(period1)] < data['ENTRY{}'.format(period2)], 1, 0)
    elif operator == "1":
        data['EntrySignal'] = np.where(data['ENTRY{}'.format(period1)] == data['ENTRY{}'.format(period2)], 1, 0)
    elif operator == "2":
        data['EntrySignal'] = np.where(data['ENTRY{}'.format(period1)] > data['ENTRY{}'.format(period2)], 1, 0)
    data['ENTRYPosition{}'.format(str(period1) + str(period2))] = data['EntrySignal'].diff()
    data.loc[data['Position'] != 1.0, ['Position']] = data['ENTRYPosition{}'.format(str(period1) + str(period2))]
    data['Position'] = data['Position'].replace([-1.0], [0.0])


def myfunc(position, exit):
    if position != -1.0:
        if position == 1.0 and exit == -1.0:
            position = 0.0
        elif position == 1.0:
            position = 1.0
        else:
            position = exit
    return position

def exitSignalGeneration(period1, period2, operator):
    global data
    if operator == "0":
        data['ExitSignal'] = np.where(data['EXIT{}'.format(period1)] < data['EXIT{}'.format(period2)], 0, 1)
    elif operator == "1":
        data['ExitSignal'] = np.where(data['EXIT{}'.format(period1)] == data['EXIT{}'.format(period2)], 0, 1)
    elif operator == "2":
        data['ExitSignal'] = np.where(data['EXIT{}'.format(period1)] > data['EXIT{}'.format(period2)], 0, 1)
    data['EXITPosition{}'.format(str(period1) + str(period2))] = data['ExitSignal'].diff()
    data['Position'] = data.apply(
        lambda x: myfunc(x['Position'], x['EXITPosition{}'.format(str(period1) + str(period2))]), axis=1)


def deploystrategyprevdaysremoval(date):
    data['Position'] = np.where(data.index < date,0.0,data['Position'])

