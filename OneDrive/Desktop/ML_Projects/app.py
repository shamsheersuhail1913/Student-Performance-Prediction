"""
PickMyGadget AI - Mobile & Laptop Recommendation System
With Advanced Filters for Better Suggestions
"""

# ==================== PIP INSTALLATIONS ====================
# pip install streamlit pandas numpy scikit-learn plotly matplotlib seaborn

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import random
import warnings
warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(
    page_title="PickMyGadget AI",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    .recommendation-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
        transition: transform 0.2s;
    }
    .recommendation-card:hover {
        transform: translateY(-5px);
    }
    .welcome-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .filter-section {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-header"><h1>🤖 PickMyGadget AI</h1><p>Smart Recommendations with Advanced Filters for Better Suggestions</p></div>', unsafe_allow_html=True)

# ==================== ENHANCED DATA GENERATION ====================
@st.cache_data
def generate_sample_data():
    """Generate comprehensive sample data with enhanced features"""
    
    # Mobile brands with their realistic model series
    mobile_brands = {
        "Apple": ["iPhone 15", "iPhone 15 Pro", "iPhone 15 Pro Max", "iPhone 14", "iPhone 14 Pro", 
                  "iPhone 13", "iPhone SE", "iPhone 14 Plus", "iPhone 15 Plus", "iPhone 12"],
        "Samsung": ["Galaxy S24", "Galaxy S24 Ultra", "Galaxy S23", "Galaxy S23 Ultra", "Galaxy A54", 
                    "Galaxy A34", "Galaxy Z Fold 5", "Galaxy Z Flip 5", "Galaxy A15", "Galaxy S24 Plus"],
        "Google": ["Pixel 8", "Pixel 8 Pro", "Pixel 7a", "Pixel 7", "Pixel Fold", "Pixel 6a", "Pixel 6"],
        "OnePlus": ["OnePlus 12", "OnePlus 12R", "OnePlus 11", "OnePlus Open", "OnePlus Nord 3", "OnePlus Nord CE 3"],
        "Xiaomi": ["Xiaomi 14", "Xiaomi 14 Ultra", "Redmi Note 13", "Redmi Note 13 Pro", "Xiaomi 13T", 
                   "Redmi 12", "Xiaomi 13", "Redmi K70"],
        "Realme": ["Realme GT 5", "Realme 12 Pro", "Realme 11 Pro", "Realme Narzo 60", "Realme C55"],
        "Vivo": ["Vivo X100", "Vivo V30", "Vivo V29", "Vivo Y100", "Vivo T2"],
        "Oppo": ["Oppo Find X7", "Oppo Reno 11", "Oppo Reno 10", "Oppo A78", "Oppo F23"],
        "Motorola": ["Moto G84", "Moto G54", "Moto Edge 40", "Moto Razr 40", "Moto G14"],
        "Nothing": ["Nothing Phone 2", "Nothing Phone 1", "Nothing Phone 2a"],
        "Sony": ["Xperia 1 V", "Xperia 5 V", "Xperia 10 V", "Xperia Pro-I"],
        "Asus": ["ROG Phone 8", "ROG Phone 7", "Zenfone 10", "Zenfone 9"],
        "LG": ["LG Velvet", "LG Wing", "LG V60", "LG G8"],
        "Huawei": ["P60 Pro", "Mate 60 Pro", "Nova 12", "Pura 70 Ultra"],
        "Nokia": ["Nokia G42", "Nokia G22", "Nokia X30", "Nokia C32"]
    }
    
    # Laptop brands with their realistic model series
    laptop_brands = {
        "Apple": ["MacBook Pro 14", "MacBook Pro 16", "MacBook Air 13", "MacBook Air 15", "MacBook Pro 13"],
        "Dell": ["XPS 13", "XPS 15", "XPS 17", "Latitude 7440", "Inspiron 16", "Alienware m18", "G15"],
        "HP": ["Spectre x360", "Envy 16", "Pavilion 15", "Omen 16", "Victus 15", "EliteBook 845"],
        "Lenovo": ["ThinkPad X1 Carbon", "ThinkPad T14", "Yoga 9i", "Legion 5 Pro", "IdeaPad Slim 5", "ThinkBook 16"],
        "Asus": ["ROG Zephyrus G14", "ROG Strix G16", "Zenbook 14", "Vivobook 15", "TUF Gaming F15"],
        "Acer": ["Swift X 14", "Predator Helios 16", "Aspire 5", "Nitro 5", "Spin 5"],
        "MSI": ["Stealth 14", "Raider GE68", "Prestige 14", "Modern 15", "Katana 15"],
        "Razer": ["Blade 14", "Blade 15", "Blade 16", "Blade 18"],
        "Microsoft": ["Surface Laptop Studio 2", "Surface Laptop 5", "Surface Pro 9", "Surface Laptop Go 3"],
        "Gigabyte": ["Aorus 15", "Aero 16", "G5", "G6"],
        "Samsung": ["Galaxy Book3 Ultra", "Galaxy Book3 Pro", "Galaxy Book4", "Galaxy Book2 Pro"],
        "LG": ["Gram 17", "Gram 16", "Gram 14", "Gram Style"],
        "Alienware": ["Alienware m16", "Alienware x16", "Alienware m18", "Alienware x14"],
        "Xiaomi": ["Redmi Book 15", "Xiaomi Book S", "Mi Notebook Pro", "Redmi G"],
        "Huawei": ["MateBook X Pro", "MateBook 14", "MateBook D16", "MateBook 16s"]
    }
    
    # Mobile processors
    mobile_processors = [
        "Apple A17 Pro", "Apple A16 Bionic", "Apple A15 Bionic", "Apple A14 Bionic",
        "Snapdragon 8 Gen 3", "Snapdragon 8 Gen 2", "Snapdragon 8 Gen 1", "Snapdragon 7 Gen 3",
        "MediaTek Dimensity 9300", "MediaTek Dimensity 9200", "MediaTek Dimensity 8300",
        "Samsung Exynos 2400", "Samsung Exynos 2200", "Google Tensor G3", "Google Tensor G2"
    ]
    
    # Laptop processors
    laptop_processors = [
        "Intel Core i9-14900HX", "Intel Core i9-13980HX", "Intel Core i7-14700HX", "Intel Core i7-13700H",
        "Intel Core i5-13500H", "Intel Core Ultra 9 185H", "Intel Core Ultra 7 155H",
        "AMD Ryzen 9 8945HS", "AMD Ryzen 9 7945HX", "AMD Ryzen 7 8845HS", "AMD Ryzen 7 7840HS",
        "Apple M3 Max", "Apple M3 Pro", "Apple M3", "Apple M2 Max", "Apple M2"
    ]
    
    # Usage types and their characteristics
    mobile_usage_types = {
        "Gaming": {"min_ram": 12, "min_refresh": 120, "min_battery": 4500},
        "Photography": {"min_camera": 50, "min_storage": 256},
        "Business": {"min_battery": 4000, "min_ram": 8, "5g_required": True},
        "Budget": {"max_price": 400},
        "Premium": {"min_price": 800, "min_ram": 12},
        "General": {}
    }
    
    laptop_usage_types = {
        "Gaming": {"min_ram": 16, "graphics_pref": ["NVIDIA RTX"], "min_price": 1000},
        "Business": {"min_battery": 60, "weight_max": 1.8, "touchscreen_pref": "No"},
        "Content Creation": {"min_ram": 32, "min_storage": 1024, "graphics_pref": ["NVIDIA RTX", "AMD Radeon"]},
        "Student": {"max_price": 800, "min_battery": 50, "weight_max": 2.0},
        "Ultrabook": {"weight_max": 1.5, "min_battery": 50, "touchscreen_pref": "Yes"},
        "General": {}
    }
    
    random.seed(42)
    np.random.seed(42)
    
    # Generate Mobile models (500+)
    mobile_models = []
    for brand, models in mobile_brands.items():
        for model in models:
            for variant in range(random.randint(3, 6)):
                ram_options = [4, 6, 8, 12, 16]
                storage_options = [64, 128, 256, 512, 1024]
                
                # Determine usage type based on specs
                ram = random.choice(ram_options)
                storage = random.choice(storage_options)
                camera = random.randint(12, 108)
                battery = random.randint(3000, 6000)
                price = random.randint(150, 1500)
                
                # Assign usage type based on specs
                if ram >= 12 and price >= 600:
                    usage = "Gaming"
                elif camera >= 50:
                    usage = "Photography"
                elif battery >= 4500 and price >= 500:
                    usage = "Business"
                elif price <= 400:
                    usage = "Budget"
                elif price >= 800:
                    usage = "Premium"
                else:
                    usage = "General"
                
                mobile_models.append({
                    'brand': brand,
                    'model': f"{model} {random.choice(['', 'Plus', 'Pro', 'Ultra', 'Max'])}".strip(),
                    'device_type': 'Mobile',
                    'price': price,
                    'ram': ram,
                    'storage': storage,
                    'battery': battery,
                    'camera_mp': camera,
                    'screen_size': round(random.uniform(5.5, 6.9), 1),
                    'processor': random.choice(mobile_processors),
                    'rating': round(random.uniform(3.2, 4.9), 1),
                    'review_count': random.randint(100, 100000),
                    'release_year': random.randint(2022, 2024),
                    '5g_support': random.choice([0, 1]),
                    'refresh_rate': random.choice([60, 90, 120, 144]),
                    'display_type': random.choice(['AMOLED', 'OLED', 'LCD', 'Retina', 'Super AMOLED']),
                    'fast_charging': random.choice([15, 25, 33, 45, 65, 100, 120]),
                    'water_resistant': random.choice(['IP67', 'IP68', 'None', 'IP54']),
                    'usage_type': usage
                })
    
    # Generate Laptop models (500+)
    laptop_models = []
    for brand, models in laptop_brands.items():
        for model in models:
            for variant in range(random.randint(3, 6)):
                ram_options = [8, 16, 32, 64, 96]
                storage_options = [256, 512, 1024, 2048, 4096]
                
                ram = random.choice(ram_options)
                storage = random.choice(storage_options)
                price = random.randint(400, 4000)
                battery = random.randint(40, 100)
                weight = round(random.uniform(1.0, 3.5), 1)
                graphics = random.choice(['Integrated', 'NVIDIA RTX 4090', 'NVIDIA RTX 4080', 'NVIDIA RTX 4070', 'NVIDIA RTX 4060', 'AMD Radeon'])
                
                # Assign usage type based on specs
                if "RTX" in graphics and ram >= 16 and price >= 1000:
                    usage = "Gaming"
                elif battery >= 60 and weight <= 1.8:
                    usage = "Business"
                elif ram >= 32 and storage >= 1024:
                    usage = "Content Creation"
                elif price <= 800 and weight <= 2.0:
                    usage = "Student"
                elif weight <= 1.5 and battery >= 50:
                    usage = "Ultrabook"
                else:
                    usage = "General"
                
                laptop_models.append({
                    'brand': brand,
                    'model': f"{model} {random.choice(['', 'Plus', 'Pro', 'Ultra', 'Max'])}".strip(),
                    'device_type': 'Laptop',
                    'price': price,
                    'ram': ram,
                    'storage': storage,
                    'battery': battery,
                    'camera_mp': random.randint(1, 8),
                    'screen_size': round(random.uniform(13, 17.3), 1),
                    'processor': random.choice(laptop_processors),
                    'rating': round(random.uniform(3.2, 4.9), 1),
                    'review_count': random.randint(100, 100000),
                    'release_year': random.randint(2022, 2024),
                    'graphics': graphics,
                    'weight_kg': weight,
                    'display_resolution': random.choice(['HD', 'Full HD', '2K', '4K', '3.2K']),
                    'touchscreen': random.choice(['Yes', 'No']),
                    'os': random.choice(['Windows 11', 'Windows 10', 'macOS', 'Linux']),
                    'usage_type': usage
                })
    
    all_devices = mobile_models + laptop_models
    df = pd.DataFrame(all_devices)
    
    # Calculate derived features
    df['value_score'] = df['rating'] * df['review_count'] / df['price']
    df['trending_score'] = df['rating'] * np.log1p(df['review_count'])
    
    # Calculate performance score
    def calculate_performance(row):
        if row['device_type'] == 'Mobile':
            processor_score = 80 if 'Snapdragon 8' in row['processor'] or 'Apple A1' in row['processor'] else 60
            return (processor_score * 0.5 + (row['ram']/16)*100*0.3 + row['rating']*20*0.2)
        else:
            processor_score = 85 if 'i9' in row['processor'] or 'Ryzen 9' in row['processor'] else 70
            return (processor_score * 0.5 + (row['ram']/64)*100*0.3 + row['rating']*20*0.2)
    
    df['performance_score'] = df.apply(calculate_performance, axis=1).round(1)
    
    return df

# Generate data
df = generate_sample_data()

# Display dataset info
st.sidebar.success(f"✅ Database Ready: {len(df)} Devices")
st.sidebar.info(f"📱 Mobiles: {len(df[df['device_type']=='Mobile'])} | 💻 Laptops: {len(df[df['device_type']=='Laptop'])}")

# ==================== DATA PREPROCESSING ====================
def preprocess_data(df):
    """Preprocess data for ML models"""
    df_processed = df.copy()
    
    le_brand = LabelEncoder()
    df_processed['brand_encoded'] = le_brand.fit_transform(df_processed['brand'].astype(str))
    
    le_processor = LabelEncoder()
    df_processed['processor_encoded'] = le_processor.fit_transform(df_processed['processor'].astype(str))
    
    feature_cols = ['price', 'ram', 'storage', 'battery', 'camera_mp', 
                   'screen_size', 'rating', 'review_count', 'release_year', 'performance_score']
    
    existing_features = [col for col in feature_cols if col in df_processed.columns]
    
    X = df_processed[existing_features].fillna(df_processed[existing_features].median())
    y_rating = df_processed['rating'].fillna(df_processed['rating'].mean())
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    return X_scaled, y_rating, df_processed, scaler, existing_features

try:
    X_scaled, y_rating, df_processed, scaler, feature_cols = preprocess_data(df)
except Exception as e:
    st.error(f"Error in preprocessing: {e}")
    st.stop()

# Train Random Forest models
@st.cache_resource
def train_models():
    try:
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_rating, test_size=0.2, random_state=42)
        rf_regressor = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
        rf_regressor.fit(X_train, y_train)
        return rf_regressor
    except Exception as e:
        st.error(f"Error training models: {e}")
        return None

rf_regressor = train_models()

# ==================== RECOMMENDATION FUNCTION WITH FILTERS ====================
def recommend_devices(user_features, device_type=None, filters=None, top_n=5):
    """Recommend devices based on user preferences and filters"""
    try:
        if device_type and device_type != "All":
            filtered_df = df_processed[df_processed['device_type'] == device_type].copy()
        else:
            filtered_df = df_processed.copy()
        
        # Apply advanced filters
        if filters:
            # Rating filter
            if filters.get('min_rating'):
                filtered_df = filtered_df[filtered_df['rating'] >= filters['min_rating']]
            
            # Usage type filter
            if filters.get('usage_type') and filters['usage_type'] != "Any":
                filtered_df = filtered_df[filtered_df['usage_type'] == filters['usage_type']]
            
            # Display type filter (mobile)
            if filters.get('display_type') and device_type == "Mobile":
                filtered_df = filtered_df[filtered_df['display_type'] == filters['display_type']]
            
            # 5G support filter (mobile)
            if filters.get('five_g') and filters['five_g'] != "Any" and device_type == "Mobile":
                filtered_df = filtered_df[filtered_df['5g_support'] == (1 if filters['five_g'] == "Yes" else 0)]
            
            # Graphics card filter (laptop)
            if filters.get('graphics') and device_type == "Laptop":
                filtered_df = filtered_df[filtered_df['graphics'].str.contains(filters['graphics'], na=False)]
            
            # Touchscreen filter (laptop)
            if filters.get('touchscreen') and filters['touchscreen'] != "Any" and device_type == "Laptop":
                filtered_df = filtered_df[filtered_df['touchscreen'] == filters['touchscreen']]
            
            # Release year filter
            if filters.get('year_range'):
                filtered_df = filtered_df[(filtered_df['release_year'] >= filters['year_range'][0]) & 
                                          (filtered_df['release_year'] <= filters['year_range'][1])]
            
            # Performance score filter
            if filters.get('min_performance'):
                filtered_df = filtered_df[filtered_df['performance_score'] >= filters['min_performance']]
            
            # Brand preference
            if filters.get('brand_preference') and filters['brand_preference'] != "Any":
                filtered_df = filtered_df[filtered_df['brand'] == filters['brand_preference']]
        
        if len(filtered_df) == 0:
            return pd.DataFrame()
        
        # Calculate scores
        scores = []
        for idx, row in filtered_df.iterrows():
            score = 0
            weight = 0
            
            if user_features.get('budget_max'):
                price = row['price']
                if price <= user_features['budget_max']:
                    score += (1 - price/user_features['budget_max']) * 30
                    weight += 30
                else:
                    score += max(0, 1 - (price - user_features['budget_max'])/user_features['budget_max']) * 20
                    weight += 20
            
            if user_features.get('min_ram') and 'ram' in row:
                if row['ram'] >= user_features['min_ram']:
                    score += 20
                    weight += 20
                else:
                    score += (row['ram']/user_features['min_ram']) * 10
                    weight += 10
            
            if user_features.get('min_storage') and 'storage' in row:
                if row['storage'] >= user_features['min_storage']:
                    score += 20
                    weight += 20
                else:
                    score += (row['storage']/user_features['min_storage']) * 10
                    weight += 10
            
            if user_features.get('min_battery') and 'battery' in row:
                if row['battery'] >= user_features['min_battery']:
                    score += 15
                    weight += 15
                else:
                    score += (row['battery']/user_features['min_battery']) * 8
                    weight += 8
            
            if user_features.get('min_camera') and 'camera_mp' in row and device_type == "Mobile":
                if row['camera_mp'] >= user_features['min_camera']:
                    score += 15
                    weight += 15
                else:
                    score += (row['camera_mp']/user_features['min_camera']) * 7
                    weight += 7
            
            # Performance score bonus
            score += row['performance_score'] * 0.5
            weight += 0.5
            
            # Value score bonus
            score += row['value_score'] * 0.3
            weight += 0.3
            
            score += row['rating'] * 10
            weight += 10
            
            normalized_reviews = np.log1p(row['review_count']) / np.log1p(df_processed['review_count'].max())
            score += normalized_reviews * 5
            weight += 5
            
            final_score = (score / weight * 100) if weight > 0 else 0
            scores.append(final_score)
        
        filtered_df['recommendation_score'] = scores
        filtered_df = filtered_df.sort_values('recommendation_score', ascending=False)
        
        return filtered_df.head(top_n)
    except Exception as e:
        st.error(f"Error in recommendation: {e}")
        return pd.DataFrame()

# ==================== SIDEBAR WITH ADVANCED FILTERS ====================
st.sidebar.markdown("## 🎯 Set Your Preferences")

# Basic Preferences
device_type = st.sidebar.selectbox("Device Type", ["All", "Mobile", "Laptop"])

budget_max = st.sidebar.slider("Maximum Budget ($)", 100, 4000, 1000, 50)

st.sidebar.markdown("### 📊 Minimum Specifications")

col1, col2 = st.sidebar.columns(2)

with col1:
    if device_type == "Mobile":
        min_ram = st.selectbox("RAM (GB)", [4, 6, 8, 12, 16], index=2)
        min_storage = st.selectbox("Storage (GB)", [64, 128, 256, 512, 1024], index=2)
    elif device_type == "Laptop":
        min_ram = st.selectbox("RAM (GB)", [8, 16, 32, 64, 96], index=1)
        min_storage = st.selectbox("Storage (GB)", [256, 512, 1024, 2048, 4096], index=1)
    else:
        min_ram = st.selectbox("RAM (GB)", [4, 6, 8, 12, 16, 32, 64, 96], index=2)
        min_storage = st.selectbox("Storage (GB)", [64, 128, 256, 512, 1024, 2048, 4096], index=2)

with col2:
    if device_type == "Mobile":
        min_battery = st.number_input("Min Battery (mAh)", 2000, 6000, 4000, 100)
        min_camera = st.number_input("Min Camera (MP)", 12, 108, 48, 12)
    elif device_type == "Laptop":
        min_battery = st.number_input("Min Battery (Wh)", 40, 100, 50, 5)
        min_camera = 0
    else:
        min_battery = st.number_input("Min Battery", 40, 6000, 2000, 100)
        min_camera = 0

# Advanced Filters Section
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔧 Advanced Filters")

# Usage Type Filter
usage_options = ["Any", "Gaming", "Photography", "Business", "Budget", "Premium", "Student", "Content Creation", "Ultrabook"]
if device_type == "Mobile":
    usage_options = ["Any", "Gaming", "Photography", "Business", "Budget", "Premium", "General"]
elif device_type == "Laptop":
    usage_options = ["Any", "Gaming", "Business", "Student", "Content Creation", "Ultrabook", "General"]

usage_type = st.sidebar.selectbox("Usage Type", usage_options)

# Rating Filter
min_rating = st.sidebar.slider("Minimum Rating", 3.0, 5.0, 3.5, 0.1)

# Performance Score Filter
min_performance = st.sidebar.slider("Minimum Performance Score", 0, 100, 60, 5)

# Brand Preference
brands = ["Any"] + sorted(df[df['device_type'] == device_type]['brand'].unique().tolist()) if device_type != "All" else ["Any"] + sorted(df['brand'].unique().tolist())
brand_preference = st.sidebar.selectbox("Preferred Brand", brands)

# Device-specific filters
if device_type in ["Mobile", "All"]:
    st.sidebar.markdown("### 📱 Mobile-Specific Filters")
    
    # 5G Support
    five_g = st.sidebar.radio("5G Support", ["Any", "Yes", "No"], horizontal=True)
    
    # Display Type
    display_type = st.sidebar.selectbox("Display Type", ["Any", "AMOLED", "OLED", "LCD", "Retina", "Super AMOLED"])

if device_type in ["Laptop", "All"]:
    st.sidebar.markdown("### 💻 Laptop-Specific Filters")
    
    # Graphics Card
    graphics_options = ["Any", "Integrated", "NVIDIA RTX", "AMD Radeon"]
    graphics = st.sidebar.selectbox("Graphics Card", graphics_options)
    
    # Touchscreen
    touchscreen = st.sidebar.radio("Touchscreen", ["Any", "Yes", "No"], horizontal=True)

# Release Year Filter
year_range = st.sidebar.slider("Release Year", 2020, 2026, (2020, 2026))

top_n = st.sidebar.slider("Number of Recommendations", 3, 15, 5)

recommend_button = st.sidebar.button("🔍 Get Recommendations", type="primary", use_container_width=True)

# ==================== MAIN CONTENT ====================
user_prefs = {
    'budget_max': budget_max,
    'min_ram': min_ram,
    'min_storage': min_storage,
    'min_battery': min_battery,
    'min_camera': min_camera if device_type == "Mobile" else None
}

filters = {
    'min_rating': min_rating,
    'usage_type': usage_type,
    'min_performance': min_performance,
    'brand_preference': brand_preference,
    'year_range': year_range
}

if device_type in ["Mobile", "All"]:
    filters['five_g'] = five_g
    filters['display_type'] = display_type if display_type != "Any" else None

if device_type in ["Laptop", "All"]:
    filters['graphics'] = graphics if graphics != "Any" else None
    filters['touchscreen'] = touchscreen if touchscreen != "Any" else None

if recommend_button:
    if rf_regressor is None:
        st.error("Models failed to load.")
    else:
        with st.spinner("🤖 AI is analyzing devices with your filters..."):
            recommendations = recommend_devices(user_prefs, device_type if device_type != "All" else None, filters, top_n)
            
            if len(recommendations) > 0:
                st.markdown("## 🎯 AI-Powered Recommendations")
                st.markdown(f"### Top {len(recommendations)} Gadgets Matching Your Criteria")
                
                # Display recommendations in columns
                cols = st.columns(min(3, len(recommendations)))
                
                for idx, (_, device) in enumerate(recommendations.iterrows()):
                    col_idx = idx % 3
                    with cols[col_idx]:
                        device_icon = '📱' if device['device_type'] == 'Mobile' else '💻'
                        storage_display = f"{device['storage']}GB" if device['storage'] < 1024 else f"{device['storage']/1024:.0f}TB"
                        
                        # Usage badge
                        usage_badge = f"🎯 {device['usage_type']}"
                        
                        st.markdown(f"""
                        <div class="recommendation-card">
                            <h3>{device_icon} {device['brand']}</h3>
                            <h4>{device['model']}</h4>
                            <p><small>{usage_badge}</small></p>
                            <hr>
                            <p>💰 Price: <strong>${device['price']:.0f}</strong></p>
                            <p>⭐ Rating: {device['rating']}/5.0 ({int(device['review_count']):,} reviews)</p>
                            <p>⚡ Performance: {device['performance_score']:.0f}/100</p>
                            <p>💾 RAM: {device['ram']}GB | Storage: {storage_display}</p>
                            <p>🔋 Battery: {device['battery']}{'mAh' if device['device_type']=='Mobile' else 'Wh'}</p>
                            <p>📱 Screen: {device['screen_size']}"</p>
                            <p>⚙️ Processor: <strong>{device['processor'][:25]}...</strong></p>
                            <p>🎯 Match Score: <strong>{device['recommendation_score']:.1f}%</strong></p>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Detailed Comparison Table
                st.markdown("## 📊 Detailed Comparison")
                
                display_cols = ['brand', 'model', 'device_type', 'usage_type', 'processor', 'price', 'ram', 'storage', 
                               'battery', 'screen_size', 'rating', 'performance_score', 'recommendation_score']
                
                display_df = recommendations[display_cols].copy()
                display_df['price'] = display_df['price'].map('${:.0f}'.format)
                display_df['rating'] = display_df['rating'].map('{:.1f}'.format)
                display_df['performance_score'] = display_df['performance_score'].map('{:.0f}/100'.format)
                display_df['recommendation_score'] = display_df['recommendation_score'].map('{:.1f}%'.format)
                display_df['storage'] = display_df['storage'].apply(lambda x: f"{x}GB" if x < 1024 else f"{x/1024:.0f}TB")
                
                st.dataframe(display_df, use_container_width=True)
                
                # Visualizations
                st.markdown("## 📈 Performance Analytics")
                
                tab1, tab2 = st.tabs(["📊 Price vs Performance", "🎯 Usage Type Distribution"])
                
                with tab1:
                    fig = px.scatter(
                        recommendations, 
                        x='price', 
                        y='performance_score', 
                        size='rating',
                        color='usage_type',
                        hover_data=['brand', 'model'],
                        title='Price vs Performance Score'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with tab2:
                    usage_counts = recommendations['usage_type'].value_counts()
                    fig = px.pie(values=usage_counts.values, names=usage_counts.index, title='Recommendations by Usage Type')
                    st.plotly_chart(fig, use_container_width=True)
                
                # Download
                st.markdown("## 💾 Download Recommendations")
                csv = recommendations.to_csv(index=False)
                st.download_button(
                    label="📥 Download as CSV",
                    data=csv,
                    file_name=f"recommendations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.warning("No devices found matching your criteria. Try adjusting your filters!")

else:
    # Home Page
    st.markdown("""
    <div class="welcome-card">
        <h1>✨ Welcome to PickMyGadget! ✨</h1>
        <p style="font-size: 1.2rem;">Find the perfect device with intelligent filters and recommendations</p>
        <p style="font-size: 1rem;">Powered by Machine Learning | 1000+ Devices | Advanced Filters</p>
        <div style="display: flex; justify-content: center; gap: 30px; margin: 30px 0;">
            <span style="font-size: 3rem;">📱</span>
            <span style="font-size: 3rem;">💻</span>
            <span style="font-size: 3rem;">🎯</span>
            <span style="font-size: 3rem;">⚡</span>
        </div>
        <p>👈 <strong>Set your preferences and advanced filters in the sidebar!</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Statistics
    st.markdown("## 📊 Database Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Devices", len(df))
    with col2:
        st.metric("Mobile Devices", len(df[df['device_type']=='Mobile']))
    with col3:
        st.metric("Laptop Devices", len(df[df['device_type']=='Laptop']))
    with col4:
        st.metric("Avg. Rating", f"{df['rating'].mean():.1f}/5")
    
    # Usage Type Distribution
    st.markdown("### 🎯 Devices by Usage Type")
    usage_counts = df.groupby(['device_type', 'usage_type']).size().reset_index(name='count')
    fig = px.bar(usage_counts, x='usage_type', y='count', color='device_type', 
                 title='Distribution of Devices by Usage Type',
                 color_discrete_map={'Mobile': '#667eea', 'Laptop': '#764ba2'})
    fig.update_layout(height=500, xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)
    
    # Performance Distribution
    st.markdown("### ⚡ Performance Score Distribution")
    fig = px.histogram(df, x='performance_score', color='device_type', nbins=30,
                       title='Performance Score Distribution',
                       color_discrete_map={'Mobile': '#667eea', 'Laptop': '#764ba2'})
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Quick Tips
    with st.expander("💡 How to Get Better Recommendations"):
        st.markdown("""
        ### 🎯 Tips for Better Results:
        
        1. **Select the Right Usage Type** - Choose what you'll primarily use the device for
        2. **Set Realistic Budget** - Be honest about your budget constraints
        3. **Use Performance Score Filter** - Higher scores indicate better overall performance
        4. **Check Device-Specific Filters** - Mobile vs Laptop have different important features
        5. **Minimum Rating** - Set at least 3.5 for reliable devices
        6. **Release Year** - Newer devices have better features and updates
        
        ### 📊 Understanding Scores:
        - **Performance Score (0-100)** - Overall device capability based on processor, RAM, and rating
        - **Match Score (%)** - How well the device matches your preferences
        - **Value Score** - Price-to-performance ratio (higher is better)
        
        ### 🔍 Advanced Filters Help:
        - **Gaming** - Look for high refresh rate, good graphics, and cooling
        - **Photography** - Focus on camera quality and storage
        - **Business** - Battery life and security features
        - **Student** - Balance of price, portability, and performance
        - **Content Creation** - High RAM, storage, and color-accurate displays
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: gray; padding: 1rem;">
    <p>🤖 AI Gadget Guide | Powered by Random Forest Algorithm | 1000+ Devices | Advanced Filters</p>
    <p>📱 Mobile: Gaming, Photography, Business, Budget, Premium | 💻 Laptop: Gaming, Business, Student, Content Creation, Ultrabook</p>
    <p>✅ Filters: Usage Type | Rating | Performance Score | Brand | 5G | Graphics | Touchscreen | Release Year</p>
    <p>Made with ❤️ using Streamlit</p>
</div>
""", unsafe_allow_html=True)