import json
import os 
import requests
from requests.auth import HTTPBasicAuth 

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

from .stock_scraper import info_scraper

# Remember that you've also added query functionality with url/stock/?company={comp_name}
def set_display(request):
    
    api_request_stock = []
    api_request_company = []
    stock = requests.get(url="http://127.0.0.1:8000/api/stock/").json()
    company = requests.get(url="http://127.0.0.1:8000/api/company/").json()

    api_request_stock.append(stock)
    api_request_company.append(company)
    while True:
        stock = requests.get(url=stock['next']).json()
        company = requests.get(url=company['next']).json()

        api_request_stock.append(stock)
        api_request_company.append(company)
        
        if stock['next'] == None and company['next'] == None:
            break 

    return render(request, 'display/home.html', context={
        'accessor_stock': api_request_stock,
        'accessor_company': api_request_company
    })

@csrf_exempt
def scrape_data(request):
    if request.user.is_superuser:
        scraped_data = info_scraper()

        headers = {'content-type': 'application/json'}
        post_request = requests.post(
        url="http://127.0.0.1:8000/api/stock/",
        json=scraped_data,
        auth=(os.environ.get('API_username'), os.environ.get('API_password')),
        headers=headers)

        return render(request, 'display/scrape.html', context={'message': 'success'})
    else:
        return render(request, 'display/scrape.html', context={
            'message': 'You aint got the permission to do that'})

def user_login(request):
    context = None 
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password') 
        auth = authenticate(request, username=username, password=password)

        if auth is not None:
            login(request, auth)
            return redirect('display_home')
        else:
            context= {'errors': 'Authentication failed, try a different username/password combination'}

    return render(request, 'display/login.html', context=context) 