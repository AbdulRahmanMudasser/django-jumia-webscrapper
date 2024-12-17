import requests
from django.shortcuts import render
from bs4 import BeautifulSoup
    
def get_content(product):
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.9"

    try:
        session = requests.Session()
        session.headers.update({
            'User-Agent': USER_AGENT,
            'Accept-Language': LANGUAGE,
            'Content-Language': LANGUAGE,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })

        response = session.get(f'https://www.jumia.com.ng/catalog/?q={product}', timeout=10)
        response.raise_for_status()

        return response.text
    except requests.RequestException as e:
        print(f"Error Fetching Data: {e}")
        
        return None

def home(request):
    product_info_list = []
    
    if 'product' in request.GET:
        product = request.GET.get('product')
        
        html_content = get_content(product=product)
        
        if html_content:
            soup = BeautifulSoup(html_content, 'html-parser')
        
            product_items = soup.find_all('article', class_='prd _fb col c-prd')
            
            for item in product_items:
                try:
                    name_tag = item.find('h3', class_='name')
                    price_tag = item.find('div', class_='prc')
                    
                    image_c_div = item.find('div', class_='img-c')
                    image_tag = image_c_div.find('img', class_='img') if image_c_div else None
                    
                    stars_div = item.find('div', class_='stars_s')
                    rating_div = stars_div.find('div', class_='in') if stars_div else None
                    
                    if name_tag and price_tag and image_tag and rating_div:
                        name = name_tag.text.strip()
                        price = price_tag.text.strip()
                        image_url = image_tag.get('data-src', '') if image_tag else ''
                        
                        rating = 'No Rating'
                        
                        if rating_div:
                            style_attribute = rating_div.get('style', '')
                            
                            if 'width' in style_attribute:
                                width_value = style_attribute.split(':')[1].replace('%', '').strip()
                                rating = f'{float(width_value) / 20:.1f}'
                        
                        product_info = {
                            'name': name,
                            'price': price,
                            'image_url': image_url,
                            'rating': rating,
                        }
                        
                        product_info_list.append(product_info)
                except Exception as e:
                    print(f'Error Processing Product: {e}')
    
    return render(request, "core/home.html", {'product_info_list': product_info_list})
