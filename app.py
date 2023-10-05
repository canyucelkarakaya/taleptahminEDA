import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Veriyi okuyun (Excel dosyanızın adını kullanın)
@st.cache_data
def load_data():
    data = pd.read_excel('tez.xlsx')
    data['Document Date'] = pd.to_datetime(data['Document Date'])
    return data

data = load_data()

# Streamlit uygulamasının başlığı
st.title("Ürün Analizi")

# İlk üç madde
st.header("1. En Çok Satılan Ürün")
most_sold_product = data.groupby('ItemCode')['Quantity'].sum().idxmax()
most_sold_quantity = data.groupby('ItemCode')['Quantity'].sum().max()
most_sold_date = data[data['ItemCode'] == most_sold_product].sort_values(by='Quantity', ascending=False)['Document Date'].iloc[0]

st.write(f"En çok satılan ürün: {most_sold_product}")
st.write(f"Toplam satış miktarı: {most_sold_quantity}")
st.write(f"En çok satış yapılan tarih: {most_sold_date}")

st.header("2. En Az Satılan Ürün")
least_sold_product = data.groupby('ItemCode')['Quantity'].sum().idxmin()
least_sold_quantity = data.groupby('ItemCode')['Quantity'].sum().min()
least_sold_date = data[data['ItemCode'] == least_sold_product].sort_values(by='Quantity', ascending=False)['Document Date'].iloc[0]

st.write(f"En az satılan ürün: {least_sold_product}")
st.write(f"Toplam satış miktarı: {least_sold_quantity}")
st.write(f"En çok satış yapılan tarih: {least_sold_date}")

st.header("3. Yıl ve Hafta Bazında Satış Analizi")
selected_year = st.selectbox("Yıl Seçin", sorted(data['Year'].unique()))
selected_week = st.selectbox("Hafta Seçin", sorted(data[data['Year'] == selected_year]['Week'].unique()))

# Belirtilen hafta yılında veri yoksa uyarı
if selected_week not in data[data['Year'] == selected_year]['Week'].unique():
    st.warning("Belirtilen hafta yılında veri bulunamadı.")
else:
    # Seçilen yıl ve hafta için en çok ve en az satılan ürünleri bulma işlemi
    filtered_data = data[(data['Year'] == selected_year) & (data['Week'] == selected_week)]
    most_sold_in_selected_period = filtered_data.groupby('ItemCode')['Quantity'].sum().idxmax()
    least_sold_in_selected_period = filtered_data.groupby('ItemCode')['Quantity'].sum().idxmin()
    
    most_sold_quantity_period = filtered_data.groupby('ItemCode')['Quantity'].sum().max()
    most_sold_date_period = filtered_data[filtered_data['ItemCode'] == most_sold_in_selected_period].sort_values(by='Quantity', ascending=False)['Document Date'].iloc[0]

    least_sold_quantity_period = filtered_data.groupby('ItemCode')['Quantity'].sum().min()
    least_sold_date_period = filtered_data[filtered_data['ItemCode'] == least_sold_in_selected_period].sort_values(by='Quantity', ascending=False)['Document Date'].iloc[0]

    st.write(f"Seçilen yılda en çok satılan ürün: {most_sold_in_selected_period}")
    st.write(f"Toplam satış miktarı: {most_sold_quantity_period}")
    st.write(f"En çok satış yapılan tarih: {most_sold_date_period}")

    st.write(f"Seçilen yılda en az satılan ürün: {least_sold_in_selected_period}")
    st.write(f"Toplam satış miktarı: {least_sold_quantity_period}")
    st.write(f"En çok satış yapılan tarih: {least_sold_date_period}")

# 4. madde
st.header("4. Ürünün Satış Tarihleri ve Miktarları")
product_name_option = st.radio("Ürünü Seçin veya Elle Girin:", ["Ürün Kodunu Girin", "Ürünü Seçin"])
if product_name_option == "Ürün Kodunu Girin":
    product_name = st.text_input("Ürün Kodunu Girin:")
    
else:
    product_name = st.selectbox("Ürünü Seçin:", sorted(data['ItemCode'].unique())) 
    
product_sales_data = data[data['ItemCode'] == product_name][['Document Date', 'Quantity']]

# Belirli bir ürünün toplam satış miktarını hesapla
total_sales_for_product = product_sales_data['Quantity'].sum()
st.write(f"Toplam Satış Miktarı: {total_sales_for_product}")

# Görselleştirme: Ürünün satış tarihleri ve miktarları
fig = px.bar(product_sales_data, x='Document Date', y='Quantity', title=f"{product_name} Satış Analizi")
st.plotly_chart(fig)



# 5. madde
st.title("5. Tarih Bazlı Günlük Toplam Satış Grafiği")

# Yıl seçimi
selected_year = st.selectbox("Yıl Seçin", sorted(data['Document Date'].dt.year.unique()), key="year_selector")

# Hafta seçimi (Tümü de dahil)
selected_week_option = st.selectbox("Hafta Seçin veya Tümü", ["Tümü"] + [str(week) for week in sorted(data[data['Year'] == selected_year]['Week'].unique())])
selected_week = None  # Başlangıçta seçilen haftayı boş olarak ayarlayın

if selected_week_option != "Tümü":
    selected_week = int(selected_week_option)  # Seçilen haftayı bir tamsayıya dönüştürün

# Veriyi haftaya göre filtreleyin
if selected_week is not None:
    data_selected_week = data[(data['Document Date'].dt.year == selected_year) & (data['Week'] == selected_week)]
    title_suffix = f" {selected_week}. Hafta"
else:
    data_selected_week = data[data['Document Date'].dt.year == selected_year]
    title_suffix = " Tüm Haftalar"

# Benzersiz tarihleri ve toplam miktarları hesaplayın
daily_total_quantity_selected_year = data_selected_week.groupby('Document Date')['Quantity'].sum()

# Toplam satış miktarını hesaplayın
total_sales_quantity = daily_total_quantity_selected_year.sum()

# Satış yapılan tarihleri ve toplam miktarları elde edin
sales_dates = daily_total_quantity_selected_year.index.strftime('%d/%m/%Y')
total_quantities = daily_total_quantity_selected_year.values

# Satış yapılan tarih sayısını hesaplayın
total_sales_count = len(sales_dates)

# Başlığı oluşturun
title = f'{selected_year} Yılında{title_suffix} Günlük Toplam Satış Grafiği\nToplam Satış: {total_sales_quantity} Adet\nToplam Satış Yapılan Tarih Sayısı: {total_sales_count}'

# Çizgi grafiği oluşturun
plt.figure(figsize=(12, 6))
plt.plot(sales_dates, total_quantities, marker='o', linestyle='-')
plt.xlabel('Satış Yapılan Tarih')
plt.ylabel('Toplam Miktar')
plt.title(title)
plt.grid(True)
plt.xticks(rotation=90)
plt.tight_layout()

# Grafiği gösterin
st.pyplot(plt.gcf())




