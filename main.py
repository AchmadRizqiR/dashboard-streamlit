import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from textblob import TextBlob
from deep_translator import GoogleTranslator



# Fungsi fungsi pertanyaan
# jawaban pertanyaan 1
@st.cache_data
def pertanyaan1():
    st.markdown('### - Heatmap Penyebaran Pelanggan')

    # Menyiapkan data untuk lattitude, longitude, dan nilai
    location = []
    df_filtered = df_geolokasi.loc[:, ['geolocation_lat', 'geolocation_lng']]

    for index, row in df_filtered.iterrows():
        location.append((
            row['geolocation_lat'],
            row['geolocation_lng'],
            1 # Value diset 1 untuk setiap customer yang melakukan pembelian di satu lokasi
            ))

    # Lat dan Long untuk lokasi dengan customer
    locations = {
        "Sao Paulo": [-23.550520, -46.633308],
        "Mexico": [19.432608, -99.133209],
        "Portugal": [39.399872, -8.224454],
        "Philippines": [12.879721, 121.774017]
    }
    # Membuat heatmap berdasarkan lokasi customer
    folium_map = folium.Map(zoom_start=5)
    HeatMap(location,radius=15).add_to(folium_map)

    # Menambah marker
    for location_name, coordinates in locations.items():
        folium.Marker(
            location=coordinates,
            popup=location_name,
            icon=folium.Icon(color="blue")
        ).add_to(folium_map)

    folium_static(folium_map) # Menampilkan heatmap

    st.markdown('### - Pie Chart Pelanggan Tiap Negara Bagian di Brazil')

    # Mengelompokkan jumlah pelanggan berdasarkan state
    df_customer_group_state = df_customer.groupby('customer_state')['customer_unique_id'].count()
    df_customer_group_state = df_customer_group_state.sort_values(ascending=False)

    # Dictionary untuk nama lengkap state
    state_mapping = {
        'SP': 'São Paulo',
        'RN': 'Rio Grande do Norte',
        'AC': 'Acre',
        'RJ': 'Rio de Janeiro',
        'ES': 'Espírito Santo',
        'MG': 'Minas Gerais',
        'BA': 'Bahia',
        'SE': 'Sergipe',
        'PE': 'Pernambuco',
        'AL': 'Alagoas',
        'PB': 'Paraíba',
        'CE': 'Ceará',
        'PI': 'Piauí',
        'MA': 'Maranhão',
        'PA': 'Pará',
        'AP': 'Amapá',
        'AM': 'Amazonas',
        'RR': 'Roraima',
        'DF': 'Distrito Federal',
        'GO': 'Goiás',
        'RO': 'Rondônia',
        'TO': 'Tocantins',
        'MT': 'Mato Grosso',
        'MS': 'Mato Grosso do Sul',
        'RS': 'Rio Grande do Sul',
        'PR': 'Paraná',
        'SC': 'Santa Catarina'
    }

    # Buat DataFrame baru dengan nama state lengkap
    df_pie = pd.DataFrame({
        "State": [state_mapping[state] for state in df_customer_group_state.index],
        "Jumlah Pelanggan": df_customer_group_state.values
    })

    # Buat Pie Chart dengan Plotly
    fig = px.pie(df_pie, names="State", values="Jumlah Pelanggan", title="Distribusi Pelanggan per State", hole=.3, height= 600)

    # Tampilkan di Streamlit
    st.plotly_chart(fig)

# Jawaban pertanyaan 2
def pertanyaan2():
    df = pd.read_csv('DataSets/order_items_dataset.csv')
    required_columns = {"shipping_limit_date", "price"}
    if required_columns.issubset(df.columns):
        df["shipping_limit_date"] = pd.to_datetime(df["shipping_limit_date"])
        df["year_month"] = df["shipping_limit_date"].dt.to_period("M")
        price_trend = df.groupby("year_month")["price"].mean().reset_index()
        price_trend["year_month"] = price_trend["year_month"].astype(str)

        st.write("**📋 Tabel Analisis: Rata-rata Harga Produk per Bulan**")
        st.dataframe(price_trend)
        
        st.write("**📊 Grafik Garis: Tren Rata-rata Harga Produk Per Bulan**")
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=price_trend, x="year_month", y="price", marker="o", linestyle="-")
        plt.xlabel("Tahun/Bulan")
        plt.ylabel("Rata-rata Harga Produk")
        plt.title("Tren Rata-rata Harga Produk Per Bulan")
        plt.xticks(rotation=45)
        plt.grid(True)
        st.pyplot(plt)

        st.write("🔍 Insight")
        st.write("Berdasarkan analisis tren harga produk per bulan, ditemukan bahwa harga mengalami fluktuasi yang menunjukkan pola kenaikan dan penurunan yang tidak selalu konsisten setiap bulan. Namun, secara keseluruhan, harga menunjukkan tren meningkat dalam jangka panjang.")
    else:
        st.error("Dataset tidak memiliki kolom yang diperlukan: 'shipping_limit_date' dan 'price'.")

# Jawaban pertanyaan 3
@st.cache_data
def pertanyaan3():
    st.title("Distribusi Skor Ulasan Pelanggan")
    st.markdown("""<hr>""",unsafe_allow_html=True)
    st.markdown("### Pertanyaan : <br>Bagaimana distribusi score ulasan pelanggan, dan apa yang dapat disimpulkan tentang tingkat kepuasan keseluruhan?<br>",unsafe_allow_html=True)

    # Check if dataset is uploaded
    df = df_review

    # Check if necessary column exists
    if "review_score" in df.columns and "review_id" in df.columns:
        # Perform grouping and analysis
        df_review_score = df.groupby('review_score')['review_id'].count().sort_index(ascending=False)
        df_review_score = df_review_score.rename('count')

        st.write(df_review_score)

        # Create pie chart
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(df_review_score, labels=df_review_score.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
        ax.set_title("Distribusi Score Ulasan Pelanggan")
        st.pyplot(fig)

        # Insights
        st.subheader("Insight")
        total_reviews = df_review_score.sum()
        highest_score = df_review_score.idxmax()
        highest_count = df_review_score.max()
        lowest_score = df_review_score.idxmin()
        lowest_count = df_review_score.min()

        st.write(f"Jumlah total ulasan: {total_reviews}")
        st.write(f"Skor ulasan tertinggi yang paling banyak diberikan adalah {highest_score} dengan jumlah {highest_count} ulasan, menyumbang {(highest_count / total_reviews * 100):.2f}% dari total ulasan.")
        st.write(f"Skor ulasan terendah adalah {lowest_score} dengan jumlah {lowest_count} ulasan, menyumbang {(lowest_count / total_reviews * 100):.2f}% dari total ulasan.")

        if highest_score == 5:
            st.write("Mayoritas pelanggan sangat puas dengan layanan atau produk yang diberikan, sebagaimana dibuktikan oleh banyaknya skor ulasan 5.")
        elif lowest_score == 1:
            st.write("Terdapat indikasi masalah signifikan karena skor ulasan 1 merupakan yang paling umum diberikan.")
        else:
            st.write("Distribusi ulasan menunjukkan variasi tingkat kepuasan pelanggan. Analisis lebih lanjut diperlukan untuk mengetahui faktor-faktor yang memengaruhi kepuasan pelanggan.")
    else:
        st.error("Kolom 'review_score' atau 'review_id' tidak ditemukan dalam dataset. Pastikan dataset memiliki kolom yang sesuai.")
        
# Jawaban pertanyaan 4
def pertanyaan4():
    st.header("Hasil Analisis")
    df = df_order
    df_order_status = df['order_status'].value_counts().reset_index()
    df_order_status.columns = ['order_status', 'count']
    df_order_status['percentage'] = df_order_status['count'] / df_order_status['count'].sum() * 100
    
    st.write("### Distribusi Status Pesanan")
    st.dataframe(df_order_status)
    
    st.write("### Visualisasi")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x='order_status', y='count', data=df_order_status, palette='viridis', ax=ax)
    ax.set_xlabel("Status")
    ax.set_ylabel("Jumlah")
    ax.set_title("Distribusi Status Pesanan")
    
    for i, row in df_order_status.iterrows():
        ax.text(i, row['count'], f"{row['count']}", ha='center', va='bottom')
    
    st.pyplot(fig)
    
    st.write("### Pilih Status Pesanan")
    selected_status = st.selectbox("Pilih status pesanan", df_order_status['order_status'].unique())
    
    filtered_data = df_order_status[df_order_status['order_status'] == selected_status]
    
    st.write(f"Jumlah order dengan status **{selected_status}**: {filtered_data['count'].values[0]}")
    st.write(f"Persentase order dengan status **{selected_status}**: {filtered_data['percentage'].values[0]:.2f}%")
    
    st.write("### Insight:")
    delivered_percentage = df_order_status[df_order_status['order_status'] == 'delivered']['percentage'].sum()
    insight_text = (
        f"Sebagian besar pesanan (**{delivered_percentage:.2f}%**) berstatus 'delivered', "
        f"menunjukkan tingkat pemenuhan pesanan yang tinggi. "
        f"Sebaliknya, beberapa status lain memiliki jumlah pesanan yang jauh lebih kecil."
    )
    st.write(insight_text)

# Jawaban pertanyaan 5
@st.cache_data
def pertanyaan5(num_top_customers):
    df_customer_order = df_customer.groupby('customer_unique_id')['customer_id'].count().sort_values(ascending=False).head(num_top_customers)
    df_customer_order = df_customer_order.rename('count')
    
    top_unique_ids = df_customer_order.index
    top_states = df_customer[df_customer['customer_unique_id'].isin(top_unique_ids)][['customer_unique_id', 'customer_state']].drop_duplicates()
    top_states.set_index('customer_unique_id', inplace=True)
    top_states = top_states.reindex(df_customer_order.index)
    
    st.write(top_states)
    
    state_colors = {
        'SP': 'red', 'MG': 'green', 'RJ': 'blue',
        'ES': 'orange', 'PE': 'yellow', 'PR': 'purple'
    }
    
    customer_colors = [state_colors.get(state, 'gray') for state in top_states['customer_state']]
    legend_handles = [mpatches.Patch(color=color, label=state) for state, color in state_colors.items()]
    
    # Visualisasi Data
    st.subheader("📊 Grafik Pembelian Per Pelanggan")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(top_unique_ids, df_customer_order.values, color=customer_colors)
    ax.set_xlabel("Jumlah Pembelian")
    ax.set_ylabel("Customer ID")
    ax.set_title("Jumlah Pembelian per Customer")
    ax.legend(handles=legend_handles, title='States')
    
    st.pyplot(fig)

# Jawaban pertanyaan 6
@st.cache_data
def pertanyaan6():
    # Pastikan kolom 'review_comment_message' ada di dataset
    if 'review_comment_message' in df_review.columns:
        # Analisis sentimen
        df_review['sentiment'] = df_review['review_comment_message'].astype(str).apply(lambda text: TextBlob(text).sentiment.polarity)
        df_review['sentiment_category'] = df_review['sentiment'].apply(lambda polarity: 'positif' if polarity > 0 else ('negatif' if polarity < 0 else 'netral'))
        
        # Hitung proporsi sentimen
        total_reviews = len(df_review)
        positive_reviews = len(df_review[df_review['sentiment_category'] == 'positif'])
        negative_reviews = len(df_review[df_review['sentiment_category'] == 'negatif'])
        neutral_reviews = len(df_review[df_review['sentiment_category'] == 'netral'])
        
        prop_pos = positive_reviews / total_reviews * 100
        prop_neg = negative_reviews / total_reviews * 100
        prop_net = neutral_reviews / total_reviews * 100
        
        # Tab tampilan
        tab1, tab2 = st.tabs(["Pertanyaan Analisis", "Analisis Sentimen"])
        
        with tab1:
            st.subheader("Pertanyaan")
            st.write('Berapa proporsi ulasan positif, negatif, dan netral dari total ulasan?')
            
        with tab2:
            st.subheader("Hasil Analisis Sentimen")
            st.write(f"Total ulasan: {total_reviews}")
            st.write(f"Proporsi ulasan positif: {prop_pos:.2f}%")
            st.write(f"Proporsi ulasan negatif: {prop_neg:.2f}%")
            st.write(f"Proporsi ulasan netral: {prop_net:.2f}%")
            
            # Pie chart
            labels = ['Positif', 'Negatif', 'Netral']
            sizes = [positive_reviews, negative_reviews, neutral_reviews]
            colors = ['green', 'red', 'yellow']
            
            fig, ax = plt.subplots()
            ax.pie(sizes, labels=labels, colors=colors, explode=(0, 0, 0.1), autopct='%1.1f%%', startangle=90)
            ax.set_title("Proporsi Ulasan")
            ax.axis('equal')  # Buat pie chart lingkaran
            
            st.pyplot(fig)
            
            # Insight
            st.subheader("Insight")
            st.write("Tingginya proporsi ulasan netral (96.47%) mengindikasikan bahwa mayoritas pelanggan memiliki pengalaman berbelanja yang cukup memuaskan. Mereka mungkin puas dengan produk atau layanan yang diterima, tetapi tidak memiliki dorongan yang kuat untuk memberikan pujian atau kritik secara eksplisit.")
            
            # Contoh ulasan dengan terjemahan
            st.subheader("Contoh Ulasan")
            
            def translate_text(text):
                try:
                    return GoogleTranslator(source='auto', target='id').translate(text)
                except:
                    return text
            
            st.write("**Ulasan Positif:**")
            positive_samples = df_review[df_review['sentiment_category'] == 'positif']['review_comment_message'].sample(3, random_state=1).tolist()
            for review in positive_samples:
                st.write(f"- {review}")
                st.write(f"  *Terjemahan:* {translate_text(review)}")
                
            st.write("**Ulasan Negatif:**")
            negative_samples = df_review[df_review['sentiment_category'] == 'negatif']['review_comment_message'].sample(3, random_state=1).tolist()
            for review in negative_samples:
                st.write(f"- {review}")
                st.write(f"  *Terjemahan:* {translate_text(review)}")
                
            st.write("**Ulasan Netral:**")
            neutral_samples = df_review[df_review['sentiment_category'] == 'netral']['review_comment_message'].sample(3, random_state=1).tolist()
            for review in neutral_samples:
                st.write(f"- {review}")
                st.write(f"  *Terjemahan:* {translate_text(review)}")







# Badan Dashboard
# Setting web page
st.set_page_config(
    page_title='Analisis E-Commerce',
    page_icon='🛍️',
    layout='wide'
)

# CSS untuk membuat konten tetap terpusat
st.markdown(
    """
    <style>
        /* Mengatur lebar maksimum dan membuat konten tetap di tengah */
        .stMainBlockContainer {
            max-width: 75rem;  /* Atur sesuai kebutuhan (900px - 1200px biasanya ideal) */
            margin-left: auto;
            margin-right: auto;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Inisialisasi session
if "current_tab" not in st.session_state:
    st.session_state.current_tab = "home"
if "show_map" not in st.session_state:
    st.session_state.show_map = False  # Menyimpan status tampilan heatmap

# Side bar 
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=['Home','Anggota','Data','Pertanyaan 1','Pertanyaan 2','Pertanyaan 3','Pertanyaan 4','Pertanyaan 5','Pertanyaan 6'],
        icons=['house','people-fill','clipboard-data','1-circle-fill','2-circle-fill','3-circle-fill','4-circle-fill','5-circle-fill','6-circle-fill'],
        default_index=0
    )
if selected == 'Home':
    st.session_state.current_tab = 'home'
if selected == 'Anggota':
    st.session_state.current_tab = 'anggota'
if selected == 'Data':
    st.session_state.current_tab = 'data'
if selected == 'Pertanyaan 1':
    st.session_state.current_tab = 'rizqi'
if selected == 'Pertanyaan 2':
    st.session_state.current_tab = 'dani'
if selected == 'Pertanyaan 3':
    st.session_state.current_tab = 'faris'
if selected == 'Pertanyaan 4':
    st.session_state.current_tab = 'reza'
if selected == 'Pertanyaan 5':
    st.session_state.current_tab = 'bastian'
if selected == 'Pertanyaan 6':
    st.session_state.current_tab = 'naufal'

# Proses Dataset
# Inisialisasi dataframe dari dataset e commerce
df_geolokasi = pd.read_csv('DataSets/geolocation_dataset.csv')
df_customer = pd.read_csv('DataSets/customers_dataset.csv')
df_review = pd.read_csv('DataSets/order_reviews_dataset.csv')
df_order = pd.read_csv('DataSets/orders_dataset.csv')

# Cleaning data review dan order
# Mengubah semua data kosong / Nan menjadi string kosong ""
df_review = df_review.fillna("")

# Mengubah tipedata dari review_creation_date dan review_answer_timestamp menjadi datetime
df_review['review_creation_date'] = pd.to_datetime(df_review['review_creation_date'])
df_review['review_answer_timestamp'] = pd.to_datetime(df_review['review_answer_timestamp'])

# Mengubah data object dengan datetime
df_order['order_delivered_carrier_date'] = pd.to_datetime(df_order['order_delivered_carrier_date'])
df_order['order_delivered_customer_date'] = pd.to_datetime(df_order['order_delivered_customer_date'])
df_order['order_estimated_delivery_date'] = pd.to_datetime(df_order['order_estimated_delivery_date'])

geolokasi_kosong = pd.DataFrame(df_geolokasi.isna().sum(), columns=['Jumlah'])
customer_kosong = pd.DataFrame(df_customer.isna().sum(), columns=['Jumlah'])
review_kosong = pd.DataFrame(df_review.isna().sum(), columns=['Jumlah'])
order_kosong = pd.DataFrame(df_order.isna().sum(), columns=['Jumlah'])

# Tab yang dipilih user
if st.session_state.current_tab == 'home':
    # Home Page
    st.title("🛍️ Dashboard Analisis E-Commerce 🛍️")
    # st.image(image='Image/Dashboard.png',use_container_width=True)
    st.markdown("""<hr>""", unsafe_allow_html=True)
    st.markdown('### Kelompok 5')
    st.markdown('### Kelas IF-5')

elif st.session_state.current_tab == 'anggota':
    # Anggota kelompok
    st.title('Anggota Kelompok:')

    cols1 = st.columns(3, gap='large', vertical_alignment='bottom')
    cols2 = st.columns(3, gap='large', vertical_alignment='bottom')
    with cols1[0]:
        with st.container(border=True):
            st.image('Image/rizqi.png', use_container_width=True)  # Gambar Portrait
            st.markdown(
                """
                <div style="
                    padding: 15px; 
                    border-radius: 10px; 
                    background-color:rgb(55, 88, 118); 
                    color:rgb(198, 227, 254);
                    font-size: 18px;
                    text-align: center;
                    margin-bottom: 1rem;">
                    Achmad Rizqi Ramadhan <br>
                    10123187<br>
                    Pertanyaan 1
                </div>
                """,
                unsafe_allow_html=True
            )
    with cols1[1]:
        with st.container(border=True):
            st.image('Image/rizqi.png', use_container_width=True)  # Gambar Portrait
            st.markdown(
                """
                <div style="
                    padding: 15px; 
                    border-radius: 10px; 
                    background-color:rgb(55, 88, 118); 
                    color:rgb(198, 227, 254);
                    font-size: 18px;
                    text-align: center;
                    margin-bottom: 1rem;">
                    Dani Andi Hendriansyah <br>
                    10123207<br>
                    Pertanyaan 2
                </div>
                """,
                unsafe_allow_html=True
            )
    with cols1[2]:
        with st.container(border=True):
            st.image('Image/rizqi.png', use_container_width=True)  # Gambar Portrait
            st.markdown(
                """
                <div style="
                    padding: 15px; 
                    border-radius: 10px; 
                    background-color:rgb(55, 88, 118); 
                    color:rgb(198, 227, 254);
                    font-size: 18px;
                    text-align: center;
                    margin-bottom: 1rem;">
                    Faris Drajat M. <br>
                    10123191<br>
                    Pertanyaan 3
                </div>
                """,
                unsafe_allow_html=True
            )

    with cols2[0]:
        with st.container(border=True):
            st.image('Image/rizqi.png', use_container_width=True)  # Gambar Portrait
            st.markdown(
                """
                <div style="
                    padding: 15px; 
                    border-radius: 10px; 
                    background-color:rgb(55, 88, 118); 
                    color:rgb(198, 227, 254);
                    font-size: 18px;
                    text-align: center;
                    margin-bottom: 1rem;">
                    M. Reza Pahlevi F.<br>
                    10123184<br>
                    Pertanyaan 4
                </div>
                """,
                unsafe_allow_html=True
            )
    with cols2[1]:   
        with st.container(border=True):
            st.image('Image/rizqi.png', use_container_width=True)  # Gambar Portrait
            st.markdown(
                """
                <div style="
                    padding: 15px; 
                    border-radius: 10px; 
                    background-color:rgb(55, 88, 118); 
                    color:rgb(198, 227, 254);
                    font-size: 18px;
                    text-align: center;
                    margin-bottom: 1rem;">
                    Bastian Van Crush <br>
                    10123174<br>
                    Pertanyaan 5
                </div>
                """,
                unsafe_allow_html=True
            )
    with cols2[2]:
        with st.container(border=True):
            st.image('Image/rizqi.png', use_container_width=True)  # Gambar Portrait
            st.markdown(
                """
                <div style="
                    padding: 15px; 
                    border-radius: 10px; 
                    background-color:rgb(55, 88, 118); 
                    color:rgb(198, 227, 254);
                    font-size: 18px;
                    text-align: center;
                    margin-bottom: 1rem;">
                    Naufal Rafi <br>
                    10123176<br>
                    Pertanyaan 6
                </div>
                """,
                unsafe_allow_html=True
            )

    
elif st.session_state.current_tab == 'data':
    # Dataset
    st.title('Dataset')
    tab1, tab2, tab3, tab4 = st.tabs(['🌎 Geolokasi','🙋‍♂️ Pelanggan','🌟 Review','🛒 Order'])
    
    with tab1:
        st.markdown('### Data Geolokasi :')
        st.dataframe(df_geolokasi)
        st.write(f'Data Kosong :')
        st.table(geolokasi_kosong)
        st.write(f'Data Duplikasi : {df_geolokasi.duplicated().sum()}')
    with tab2:
        st.markdown('### Data Customer :')
        st.dataframe(df_customer)
        st.write(f'Data Kosong :')
        st.table(customer_kosong)
        st.write(f'Data Duplikasi : {df_customer.duplicated().sum()}')
    with tab3:
        st.markdown('### Data Review :')
        st.dataframe(df_review)
        st.write(f'Data Kosong :')
        st.table(review_kosong)
        st.write(f'Data Duplikasi : {df_review.duplicated().sum()}')
    with tab4:
        st.markdown('### Data Order :')
        st.dataframe(df_order)
        st.write(f'Data Kosong :')
        st.table(order_kosong)
        st.write(f'Data Duplikasi : {df_order.duplicated().sum()}')

elif st.session_state.current_tab == 'rizqi':
    # Pertanyaan rizqi
    st.title('Penyebaran Pelanggan 🙋‍♂️')

    # Navbar
    tab1, tab2, tab3, tab4 = st.tabs(['❓Pertanyaan','🔎Langkah Penyelesaian','</>Cuplikan Kode','📚Hasil Analisis'])
    # tab_rizqi = option_menu(
    #     menu_title=None,
    #     options=['Pertanyaan','Langkah Penyelesaian','Cuplikan Kode','Jawaban'],
    #     icons=['question-diamond','journal-check','code-slash','lightbulb-fill'],
    #     orientation='horizontal'
    # )

    st.markdown("""<br>""", unsafe_allow_html=True)

    with tab1:
        st.markdown('### ❓Pertanyaan : \n'
                 'Bagaimana distribusi geografis pelanggan berdasarkan negara bagian dan kota di dunia? Dimanakah tingkat konsentrasi tertinggi pelanggan berada?')
    
    with tab2:
        st.markdown('### 🔎Langkah - langkah penyelesaian')
        st.image("Image/Langkah.png", use_container_width=True)

    with tab3:
        # Menampilkan cuplikan kode
        # Kode untuk menyiapkan lokasi heatmap
        st.markdown("### Menyiapkan Lokasi Customer Untuk Heatmap")
        st.code(
            """
                # Menyiapkan data untuk lattitude, longitude, dan nilai
                location = []
                df_filtered = df_geolokasi.loc[:, ['geolocation_lat', 'geolocation_lng']]

                for index, row in df_filtered.iterrows():
                    location.append((
                        row['geolocation_lat'],
                        row['geolocation_lng'],
                        1 # Value diset 1 untuk setiap customer yang melakukan pembelian di satu lokasi
                    ))
            """, language="python"
        )

        # Kode untuk titik di heatmap
        st.markdown('### Menyiapkan Titik Untuk Heatmap')
        st.code(
            """
                # Lat dan Long untuk lokasi dengan customer
                locations = {
                    "Sao Paulo": [-23.550520, -46.633308],
                    "Mexico": [19.432608, -99.133209],
                    "Portugal": [39.399872, -8.224454],
                    "Philippines": [12.879721, 121.774017]
                }
            """,language="python"
        )

        # kode untuk menampilkan heatmap
        st.markdown("### Menampilkan Heatmap")
        st.code(
            """
                # Membuat heatmap berdasarkan lokasi customer
                folium_map = folium.Map(zoom_start=5)
                HeatMap(location,radius=15).add_to(folium_map)

                # Menambah marker
                for location_name, coordinates in locations.items():
                    folium.Marker(
                        location=coordinates,
                        popup=location_name,
                        icon=folium.Icon(color="blue")
                    ).add_to(folium_mapmap)

                folium_static(folium_map)
            """,language="python"
        )

        # kode untuk menyiapkan dataset pie chart
        st.markdown("### Menyiapkan Data Piechart")
        st.code(
            """
                # Mengelompokkan jumlah pelanggan berdasarkan state
                df_customer_group_state = df_customer.groupby('customer_state')['customer_unique_id'].count()
                df_customer_group_state = df_customer_group_state.sort_values(ascending=False)

                # Dictionary untuk nama lengkap state
                state_mapping = {
                    'SP': 'São Paulo',
                    'RN': 'Rio Grande do Norte',
                    'AC': 'Acre',
                    'RJ': 'Rio de Janeiro',
                    'ES': 'Espírito Santo',
                    'MG': 'Minas Gerais',
                    'BA': 'Bahia',
                    'SE': 'Sergipe',
                    'PE': 'Pernambuco',
                    'AL': 'Alagoas',
                    'PB': 'Paraíba',
                    'CE': 'Ceará',
                    'PI': 'Piauí',
                    'MA': 'Maranhão',
                    'PA': 'Pará',
                    'AP': 'Amapá',
                    'AM': 'Amazonas',
                    'RR': 'Roraima',
                    'DF': 'Distrito Federal',
                    'GO': 'Goiás',
                    'RO': 'Rondônia',
                    'TO': 'Tocantins',
                    'MT': 'Mato Grosso',
                    'MS': 'Mato Grosso do Sul',
                    'RS': 'Rio Grande do Sul',
                    'PR': 'Paraná',
                    'SC': 'Santa Catarina'
                }
            """,language="python"
        )

        # kode untuk menampilkan PieChart
        st.markdown("### Menampilkan Pie Chart")
        st.code(
            """
                # Buat DataFrame baru dengan nama state lengkap
                df_pie = pd.DataFrame({
                    "State": [state_mapping[state] for state in df_customer_group_state.index],
                    "Jumlah Pelanggan": df_customer_group_state.values
                })

                # Buat Pie Chart dengan Plotly
                fig = px.pie(df_pie[:5], names="State", values="Jumlah Pelanggan", title="Distribusi Pelanggan per State", hole=.3, height= 600)

                # Tampilkan di Streamlit
                st.plotly_chart(fig)
            """,language="python"
        )

    with tab4:
        if st.button("Tampilkan Hasil Analisis"):
            st.session_state.show_map = True  # Update state agar heatmap ditampilkan

        # Tampilkan heatmap hanya jika tombol ditekan
        if st.session_state.show_map:
            pertanyaan1()
        
elif st.session_state.current_tab == 'dani':
    st.title("📊 Dashboard Analisis E-Commerce")
    tab1, tab2, tab3, tab4 = st.tabs(["❓Pertanyaan", "🛠️Langkah Analisis", "</> Cuplikan Kode", "📊 Analisis Data"])  

    with tab1:
        st.subheader("❓ Pertanyaan Analisis")
        st.write("Bagaimana tren rata-rata harga produk per bulan? Apakah ada pola kenaikan atau penurunan harga dalam periode tertentu?")

    with tab2:
        st.subheader("🛠️ Langkah Analisis")
        st.write("1. Menyiapkan dataset CSV yang diperlukan.")
        st.write("2. Mengonversi kolom tanggal pengiriman ke format datetime.")
        st.write("3. Mengelompokkan harga produk berdasarkan bulan dan tahun.")
        st.write("4. Menampilkan tabel rata-rata harga per bulan.")
        st.write("5. Membuat grafik tren harga untuk visualisasi.")
        st.write("6. Memberikan insight berdasarkan hasil analisis.")

    with tab3:   
        st.subheader("</> Cuplikan Kode")
        
        st.write("Konversi tanggal ke format datetime")
        st.code(
            '''
            df["shipping_limit_date"] = pd.to_datetime(df["shipping_limit_date"])
            df["year_month"] = df["shipping_limit_date"].dt.to_period("M")
            price_trend = df.groupby("year_month")["price"].mean().reset_index()
            price_trend["year_month"] = price_trend["year_month"].astype(str)
            ''',
            language="python"
        )

        st.write("Menampilkan table analisis")
        st.code(
            '''
            st.write("**📋 Tabel Analisis: Rata-rata Harga Produk per Bulan**")
            st.dataframe(price_trend)
            ''',
            language="python"
        )

        st.write("Membuat grafik tren untuk visualisasi")
        st.code(
            '''
            st.write("**📊 Grafik Garis: Tren Rata-rata Harga Produk Per Bulan**")
                plt.figure(figsize=(12, 6))
                sns.lineplot(data=price_trend, x="year_month", y="price", marker="o", linestyle="-")
                plt.xlabel("Tahun/Bulan")
                plt.ylabel("Rata-rata Harga Produk")
                plt.title("Tren Rata-rata Harga Produk Per Bulan")
                plt.xticks(rotation=45)
                plt.grid(True)
                st.pyplot(plt)
            ''',
            language="python"
        )

        st.write("Memberikan insight terhadap hasil analisis")
        st.code(
            '''
            st.subheader("🔍 Insight")
            st.write("Berdasarkan analisis tren harga produk per bulan, ditemukan bahwa harga mengalami fluktuasi yang menunjukkan pola kenaikan dan penurunan yang tidak selalu konsisten setiap bulan. Namun, secara keseluruhan, harga menunjukkan tren meningkat dalam jangka panjang.")
            ''',
            language="python"
        )
    with tab4:
        pertanyaan2()
elif st.session_state.current_tab == 'faris':
    pertanyaan3()

elif st.session_state.current_tab == 'reza':
    tab1, tab2, tab3 = st.tabs(["📌 Pertanyaan", "📜 Kode", "📊 Hasil Analisis"])
    with tab1:
        st.header("Bagaimana distribusi Status Pesanan, dan berapa persentase order dengan status 'delivered'❓")

    with tab2:
        st.header("Menghitung jumlah order per status")
        st.code(
            """
            df_order_status = df['order_status'].value_counts().reset_index()
            df_order_status.columns = ['order_status', 'count']
            df_order_status['percentage'] = df_order_status['count'] / df_order_status['count'].sum() * 100

            
            """, language="python"
        )

        st.header("Distribusi Status Pesanan")
        st.code(
            """
            st.dataframe(df_order_status)
        """,language="python"
        )
            
        st.header("Visualisasi")
        st.code(
            """
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.barplot(x='order_status', y='count', data=df_order_status, palette='viridis', ax=ax)
            ax.set_xlabel("Status")
            ax.set_ylabel("Jumlah")
            ax.set_title("Distribusi Status Pesanan")
            for i, row in df_order_status.iterrows():
                ax.text(i, row['count'], f"{row['count']}", ha='center', va='bottom')
            
            st.pyplot(fig)
            """, language="python"
            )

    with tab3:
        pertanyaan4()


elif st.session_state.current_tab == 'bastian':
    st.title("📊 Dashboard Analisis Loyalitas Pelanggan")
    st.write("Pelanggan mana yang melakukan pembelian berulang, dan apakah pola ini menunjukkan loyalitas pelanggan di negara bagian tertentu?")
    
    # Menampilkan tabel data
    st.subheader("📌 Data Top Pelanggan")
    
    # Menampilkan filter di bawah
    st.markdown("---")
    st.subheader("🔍 Filter Data")
    num_top_customers = st.slider("Jumlah Pelanggan Teratas", 5, 20, 10)
    
    pertanyaan5(num_top_customers)

elif st.session_state.current_tab == 'naufal':
    pertanyaan6()
