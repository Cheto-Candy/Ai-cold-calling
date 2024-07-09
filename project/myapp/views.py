# views.py
import requests
from .models import Lead
from django.shortcuts import render,redirect
from .forms import FetchCallSummaryForm,Fetchcallanalyticsform,createcallform
from myapp import api
from datetime import datetime,time
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

























def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout
# Dashboard view (protected)











# views.py
@login_required
def dashboard(request):
    today = datetime.now().date()
    leads_today = Lead.objects.filter(call_date=today)
    # today = datetime.now().date()
    # leads_today = Lead.objects.filter(call_id__date=today)
    total_calls_today = leads_today.count()
    total_converted_leads_today = leads_today.filter(converted=True).count()

    # Prepare data for the graph
    call_data = {
        'total_calls_today': total_calls_today,
        'converted_leads_today': total_converted_leads_today
    }

    context = {
        'call_data': call_data,
        'total_calls_today': total_calls_today,
        'total_converted_leads_today': total_converted_leads_today,
    }

    return render(request, 'dashboard.html', context)
# @login_required
def fetch_call_summary(request):
    if request.method == 'POST':
        form = FetchCallSummaryForm(request.POST)
        if form.is_valid():
            call_id = form.cleaned_data['call_id']
            summary = api.get_call_summary_from_vapi(call_id)
            context ={
                    'summary':summary,
                    'call_id':call_id
                }
            return render(request, 'summary.html', context)
            # return HttpResponse(f"Call Summary: {summary}")
    else:
        form = FetchCallSummaryForm()
    
    return render(request, 'fetch_call_summary.html', {'form': form})
# @login_required
def create_call(request):
    if request.method == 'POST':
        form = createcallform(request.POST)
        if form.is_valid():

            while True:
                lead=api.ectrct_lead(form)
                if 'phone' and 'name' in lead:
                    break    
            purpose=api.create_a_purpose(lead)
            name = lead['name']
            number = lead['phone']
            print(purpose,lead,name,number)
            call_id =api.create_a_call(purpose,name,number)
            _=api.wait_for_call_completion(call_id)
            summary = api.get_call_summary_from_vapi(call_id)
            analytics=api.fetch_call_analytics_from_vapi(call_id)
            converted_or_not=api.check_lead(summary)
            if converted_or_not == 1:
                converted = True
            else:
                converted = False

            # Save to the database
            lead_record = Lead(
                name=name,
                phone=number,
                call_id=call_id,
                purpose=purpose,
                summary=summary,
                analytics=analytics,
                converted=converted
            )
            lead_record.save()

            context = {
                'lead_converted': 'lead is converted' if converted else 'lead is not converted',
                'analytics': {
                    'summary': summary,
                    'details': analytics
                }
            }
            return render(request, 'call_result.html', context)

    else:
        form = createcallform()
    
    return render(request, 'create_call.html', {'form': form})
# @login_required
def fetch_call_analytics(request):
    if request.method == 'POST':
        form = Fetchcallanalyticsform(request.POST)
        if form.is_valid():
            call_id = form.cleaned_data['call_id']
            analytics = api.fetch_call_analytics_from_vapi(call_id)
            context ={
                    'call_id':call_id,
                    'cost':analytics.get('cost'),
                    'duration':analytics.get('duration'),
                    'status':analytics.get('status')                    
                }
            return render(request, 'analytics.html', context)

    else:
        form = Fetchcallanalyticsform()
    
    return render(request, 'fetch_call_analytics.html', {'form': form})

