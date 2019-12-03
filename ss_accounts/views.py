from django.shortcuts import render,redirect
from django.contrib import auth
from django.http import HttpResponse
from superstocks.models import SuperStokist
import csv, io
from .models import csv_data
from .models import temp_ssdata
from random import randint
import re
import django

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
# Create your views here.


def logout(request):
    auth.logout(request)
    return redirect('/ss_accounts/login')


def login(request):
    # logout(request)
    # username = password = ''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            
            django.contrib.auth.login(request, user)
            return redirect('dashboard')
        else:
            return HttpResponse("Sorry")    
    #   obj = SuperStokist.objects.all()
    #     name = [nam.Stockist_Name for nam in obj]
    #     pswd =[pas.Password for pas in obj]
        # print(name)
        # print(pswd)
        # print(obj)    
        # print(username)
        # print(password)
        # rndm_no = randint(0,1000)
        # if (username in name) and (password in pswd):
        #     return redirect('dashboard', id=username+str(rndm_no))

    return render(request, 'ss_accounts/login.html')


@login_required(login_url='/ss_accounts/login/')
def dash(request):
    if request.user.is_superuser:
        return redirect('/admin/')

    # print('XXXXXXXXXXXXXXXXXXXXXXXXXXXX',request.user)
    id = request.user
    print('------------------',id)
    
    # return render(request,'ss_accounts/ss_dashboard.html')    
    template = "ss_accounts/ss_dashboard.html"

    prompt = {
        'order': 'upload your csv properly'
    }

    if request.method == "GET":

        return render(request, template)
    # ####### if the file is GLOBAL
    if 'file2' in request.FILES:
        csv_file = request.FILES['file2']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'this is not csv file')
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)
        # print(data_set)
        # if data in database is not empty
        obj = csv_data.objects.all()
        # ss = obj[0].SSname
        # print(ss)
        ss_name = [ss.SSname for ss in obj]
        print('JJJJJJJJJJJJJJJJJJJJJJ', ss_name, month, id)
        # ############################## condition if selected SS data exist ######
        if (len(ss_name) > 0 and (str(id) in ss_name)):
            # print(obj)
            # obj.delete() # deleting all obj if exists
            # dumping in temdb

            for i in range(0, len(ss_name)):
                if (obj[i].SSname == str(id) and obj[i].month == ''):
                    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXX', obj[i].SSname, 'month:', obj[i].month)
                    _, created = temp_ssdata.objects.update_or_create(
                            SSname=obj[i].SSname,
                            Route=obj[i].Route,
                            District=obj[i].District,
                            Town=obj[i].Town,
                            Day=obj[i].Day,
                            Supervisor=obj[i].Supervisor,
                            VSR=obj[i].VSR,
                            Contact=obj[i].Contact
                            )
                        
            obj.filter(SSname=id, month='').delete()  # delete all obj of logedin ss
            for column in csv.reader(io_string, delimiter=',', quotechar="|"):
                # print(column[0])
                if len(column) == 0:
                    break
                else:
                    _, created = csv_data.objects.update_or_create(
                        SSname=str(id),
                        Route=int(column[0]),
                        District=str(column[1]),
                        Town=int(column[2]),
                        Day=int(column[3]),
                        Supervisor=str(column[4]),
                        VSR=str(column[5]),
                        Contact=int(column[6])
                        )
            context = {'message': 'hey buddy new data uploaded your data'}
            return render(request, template, context)
        
        # ########################### if SS data in database is not there    
        else:
            for column in csv.reader(io_string, delimiter=',', quotechar="|"):
                # print(column[0])
                if len(column) == 0:
                    break
                else:
                    _, created = csv_data.objects.update_or_create(
                        SSname=str(id),
                        Route=int(column[0]),
                        District=str(column[1]),
                        Town=int(column[2]),
                        Day=int(column[3]),
                        Supervisor=str(column[4]),
                        VSR=str(column[5]),
                        Contact=int(column[6])
                        )
            context = {'message': 'hey buddy uploaded your data'}
            return render(request, template, context)        
    
    # if the file is for a month
    if 'file3' in request.FILES:
        csv_file = request.FILES['file3']
        u_month = request.POST['selected_month']
        print('this is month user entered -------', u_month)
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'this is not csv file')
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)

        obj = csv_data.objects.all()
        # ss = obj[0].SSname
        # print(ss)
        ss_name = [ss.SSname for ss in obj]
        print('JJJJJJJJJJJJJJJJJJJJJJ', ss_name, id)
        # ############################## condition if selected SS data exist ######
        if (len(ss_name) > 0 and (str(id) in ss_name)):
            # print(obj)
            # obj.delete() # deleting all obj if exists
            # dumping in temdb

            for i in range(0, len(ss_name)):
                if (obj[i].SSname == str(id) and obj[i].month != ''):
                    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXX', obj[i].SSname, obj[i].month)
                    _, created = temp_ssdata.objects.update_or_create(
                            SSname=obj[i].SSname,
                            Route=obj[i].Route,
                            District=obj[i].District,
                            Town=obj[i].Town,
                            Day=obj[i].Day,
                            Supervisor=obj[i].Supervisor,
                            VSR=obj[i].VSR,
                            Contact=obj[i].Contact,
                            month=obj[i].month
                            )
                        
            obj.filter(SSname=id).exclude(month='').delete()  # delete all obj of logedin ss
            for column in csv.reader(io_string, delimiter=',', quotechar="|"):
                # print(column[0])
                if len(column) == 0:
                    break
                else:
                    _, created = csv_data.objects.update_or_create(
                        SSname=str(id),
                        Route=int(column[0]),
                        District=str(column[1]),
                        Town=int(column[2]),
                        Day=int(column[3]),
                        Supervisor=str(column[4]),
                        VSR=str(column[5]),
                        Contact=int(column[6]),
                        month=u_month
                        )
            context = {'message': 'hey buddy new data uploaded your data'}
            return render(request, template, context)
        
        # ########################### if SS data in database is not there    
        else:
            for column in csv.reader(io_string, delimiter=',', quotechar="|"):
                # print(column[0])
                if len(column) == 0:
                    break
                else:
                    _, created = csv_data.objects.update_or_create(
                        SSname=str(id),
                        Route=int(column[0]),
                        District=str(column[1]),
                        Town=int(column[2]),
                        Day=int(column[3]),
                        Supervisor=str(column[4]),
                        VSR=str(column[5]),
                        Contact=int(column[6]),
                        month=u_month
                        )
        context = {'message': 'hey buddy uploaded your new month data data'}
        return render(request, template, context)