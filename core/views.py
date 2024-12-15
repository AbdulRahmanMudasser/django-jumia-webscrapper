from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

def get_content(product):
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/437.36"
    LANGUAGE = "en-US,en;q-0.5"
    
    session = requests.Session
    
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE 
    session.headers['Content-Language'] = LANGUAGE 
    
    html_content = session.get(f'https://www.jumia.com.ng/catalog/?q={product}')

def home(request):
    product_info_list = []
    
    if 'products' in request.GET:
        product = request.GET.get('product')
        
        html_content = get_content(product=product)
    
    return render(request, "core/home.html")
