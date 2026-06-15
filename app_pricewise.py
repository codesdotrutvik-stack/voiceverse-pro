import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

st.set_page_config(page_title="PriceWise AI", page_icon="💰", layout="wide")

st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
    }
    .main-header h1 { color: white; margin: 0; }
    .product-card {
        background: white;
        border-radius: 16px;
        padding: 1rem;
        margin: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .price { font-size: 1.5rem; font-weight: 700; color: #10b981; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>💰 PriceWise AI</h1>
    <p>Real-time price comparison • Amazon • Flipkart • (More coming soon)</p>
</div>
""", unsafe_allow_html=True)

SCRAPERAPI_KEY = "9ea5089dc009873729dc7e2a201376ff"

def scrape_amazon(product_name):
    search_url = f"https://www.amazon.in/s?k={product_name.replace(' ', '+')}"
    api_url = f"https://api.scraperapi.com?api_key={SCRAPERAPI_KEY}&url={search_url}&render=true"
    
    try:
        response = requests.get(api_url, timeout=30)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            products = []
            
            containers = soup.find_all("div", {"data-component-type": "s-search-result"})
            
            for container in containers[:10]:
                try:
                    name_elem = container.find("span", class_="a-size-medium")
                    if not name_elem:
                        name_elem = container.find("span", class_="a-size-base-plus")
                    
                    price_elem = container.find("span", class_="a-price-whole")
                    
                    if name_elem and price_elem:
                        name = name_elem.text.strip()
                        price_num = int(price_elem.text.strip().replace(',', ''))
                        
                        rating_elem = container.find("span", class_="a-icon-alt")
                        rating = rating_elem.text.split()[0] if rating_elem else "4.0"
                        
                        products.append({
                            "name": name[:60],
                            "price": price_num,
                            "price_display": f"₹{price_num:,}",
                            "rating": rating,
                            "store": "Amazon"
                        })
                except:
                    continue
            return products
        return []
    except Exception as e:
        st.error(f"Amazon error: {e}")
        return []

# Mock Flipkart data (temporary fix)
def get_mock_flipkart(product_name):
    return [
        {"name": f"{product_name} (Mock)", "price": 45999, "price_display": "₹45,999", "rating": "4.3", "store": "Flipkart"},
        {"name": f"{product_name} Pro (Mock)", "price": 52999, "price_display": "₹52,999", "rating": "4.5", "store": "Flipkart"},
    ]

col1, col2 = st.columns([3, 1])

with col1:
    search_query = st.text_input("", placeholder="🔍 Search product... (e.g., iPhone 14, Samsung Galaxy)", label_visibility="collapsed")

with col2:
    search_btn = st.button("🔍 Compare", use_container_width=True)

if search_btn and search_query:
    all_products = []
    
    with st.spinner(f"Searching for '{search_query}'..."):
        st.write("📦 Scraping Amazon...")
        amazon_products = scrape_amazon(search_query)
        all_products.extend(amazon_products)
        
        st.write("🛍️ Flipkart (Demo data)...")
        flipkart_products = get_mock_flipkart(search_query)
        all_products.extend(flipkart_products)
    
    if all_products:
        st.success(f"✅ Found {len(all_products)} products")
        
        all_products.sort(key=lambda x: x['price'])
        
        st.markdown("---")
        st.subheader("📊 Price Comparison")
        
        cols = st.columns(min(len(all_products), 4))
        for i, product in enumerate(all_products[:4]):
            with cols[i % 4]:
                st.markdown(f"""
                <div class="product-card">
                    <h4>{product['store']}</h4>
                    <div class="price">{product['price_display']}</div>
                    <p>⭐ {product['rating']} ★</p>
                    <p style="font-size:0.8rem">{product['name'][:30]}</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("📋 Complete Table")
        
        df = pd.DataFrame(all_products)
        st.dataframe(df[["store", "name", "price_display", "rating"]], use_container_width=True)
        
        best = all_products[0]
        st.success(f"🏆 **Best Deal:** {best['store']} at {best['price_display']}")
        
    else:
        st.error(f"No products found for '{search_query}'")

st.markdown("---")
st.caption("Made with ❤️ using ScraperAPI | PriceWise AI")