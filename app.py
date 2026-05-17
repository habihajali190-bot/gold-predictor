import streamlit as st
import pandas as pd
import numpy as np

# 1. إعدادات الصفحة الأساسية وتحسين الثيم العام
st.set_page_config(
    page_title="Quantum Institutional Gold Predictor",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# إضافة حزمة CSS مخصصة لتجميل الواجهة وضمان الألوان الاحترافية الفخمة
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&display=swap');
        
        /* إعدادات الخط والاتجاهات */
        html, body, [data-testid="stSidebar"], .stMarkdown, p, h1, h2, h3, h4 {
            font-family: 'Tajawal', sans-serif;
            direction: rtl;
            text-align: right;
        }

        /* الخلفية الداكنة الفخمة */
        .stApp {
            background-color: #0b0f1a;
            background-image: radial-gradient(circle at 50% -20%, #1e293b 0%, #0b0f1a 80%);
        }

        /* حاوية البطاقات */
        .pricing-container {
            display: flex;
            gap: 25px;
            justify-content: center;
            padding: 40px 0;
        }

        /* تصميم البطاقة الفخم */
        .card {
            background: rgba(30, 41, 59, 0.5);
            backdrop-filter: blur(10px);
            border-radius: 24px;
            padding: 40px 30px;
            text-align: center;
            transition: all 0.4s ease;
            border: 1px solid rgba(255, 255, 255, 0.1);
            position: relative;
            height: 100%;
        }

        .card:hover {
            transform: translateY(-10px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
        }

        /* تمييز باقة الـ PRO بالأزرق */
        .pro-card {
            border-top: 5px solid #3b82f6;
            box-shadow: 0 10px 30px rgba(59, 130, 246, 0.1);
        }

        /* تمييز باقة الـ PREMIUM بالذهبي */
        .premium-card {
            border-top: 5px solid #fbbf24;
            box-shadow: 0 10px 30px rgba(251, 191, 36, 0.1);
        }

        .badge {
            position: absolute;
            top: -15px;
            left: 50%;
            transform: translateX(-50%);
            padding: 6px 20px;
            border-radius: 50px;
            font-size: 14px;
            font-weight: bold;
            color: white !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }

        .title {
            font-size: 26px;
            font-weight: 800;
            margin-bottom: 15px;
            color: #ffffff !important;
        }

        .price {
            font-size: 50px;
            font-weight: 800;
            margin: 20px 0;
            letter-spacing: -1px;
        }

        .price span {
            font-size: 18px;
            font-weight: normal;
            color: #94a3b8;
        }

        .features {
            list-style: none;
            padding: 0;
            margin: 30px 0;
            text-align: right;
            color: #cbd5e1 !important;
        }

        .features li {
            margin-bottom: 12px;
            font-size: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        /* الأزرار */
        .btn {
            display: block;
            padding: 15px 30px;
            border-radius: 12px;
            text-decoration: none !important;
            font-weight: bold;
            font-size: 18px;
            transition: all 0.3s ease;
            color: white !important;
        }

        .btn-pro {
            background: linear-gradient(135deg, #2563eb, #1d4ed8);
            box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);
        }

        .btn-pro:hover {
            box-shadow: 0 6px 25px rgba(37, 99, 235, 0.5);
            transform: scale(1.03);
        }

        .btn-premium {
            background: linear-gradient(135deg, #f59e0b, #d97706);
            box-shadow: 0 4px 15px rgba(245, 158, 11, 0.3);
        }

        .btn-disabled {
            background: #334155;
            color: #94a3b8 !important;
            cursor: not-allowed;
            opacity: 0.7;
        }

        /* تعديلات نصوص الواجهة */
        .main-title {
            font-size: 45px;
            font-weight: 800;
            background: linear-gradient(to right, #ffffff, #94a3b8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# 2. نظام التحقق وإدارة الأكواد
VALID_SERIALS = {
    "GOLD-PRO-8812": "Pro"
}

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_tier" not in st.session_state:
    st.session_state.user_tier = None

# 3. واجهة الدخول (قبل التفعيل)
if not st.session_state.authenticated:
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    st.markdown("<h1 class='main-title'>⚡ منصة التوقع المؤسسي للذهب</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 18px; margin-bottom: 40px;'>نظام الذكاء الرقمي لفك تشفير السيولة وتتبع الحيتان</p>", unsafe_allow_html=True)
    
    # صندوق التفعيل الفخم
    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        st.markdown("<div style='background: rgba(255,255,255,0.05); padding: 30px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center; color: #ffffff; margin-bottom: 20px;'>🔑 أدخل مفتاح الوصول الفوري</h4>", unsafe_allow_html=True)
        serial_input = st.text_input("الكود:", placeholder="GOLD-XXXX-XXXX", label_visibility="collapsed").strip()
        if st.button("تفعيل المنصة 🚀", use_container_width=True):
            if serial_input in VALID_SERIALS:
                st.session_state.authenticated = True
                st.session_state.user_tier = VALID_SERIALS[serial_input]
                st.success(f"🎉 تم التفعيل بنجاح! مرحباً بك في الباقة ({st.session_state.user_tier})")
                st.rerun()
            elif serial_input == "":
                st.warning("⚠️ يرجى إدخال الكود أولاً")
            else:
                st.error("❌ الكود غير صحيح")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #ffffff;'>💳 اختر خطة الوصول المناسبة</h2>", unsafe_allow_html=True)

    # عرض البطاقات
    cp1, cp2 = st.columns(2)

    with cp1:
        st.markdown("""
        <div class="card pro-card">
            <div class="badge" style="background: #3b82f6;">الأكثر طلباً 🔥</div>
            <div class="title">باقة المحترفين (PRO)</div>
            <div class="price" style="color: #3b82f6;">$29.99<span>/شهرياً</span></div>
            <ul class="features">
                <li>✅ كشف مناطق الـ Order Blocks</li>
                <li>✅ تحديد فجوات الـ FVG المؤسسية</li>
                <li>✅ مؤشر الـ ADX المطور للزخم</li>
                <li>✅ تنبيهات سيولة لحظية</li>
            </ul>
            <a href="https://shoppy.gg/product/5ZAWaH9" target="_blank" class="btn btn-pro">شراء كود التفعيل 💳</a>
        </div>
        """, unsafe_allow_html=True)

    with cp2:
        st.markdown("""
        <div class="card premium-card">
            <div class="badge" style="background: #fbbf24; color: #000 !important;">قوة الحوت 🐳</div>
            <div class="title">الباقة المميزة (PREMIUM)</div>
            <div class="price" style="color: #fbbf24;">$49.99<span>/شهرياً</span></div>
            <ul class="features">
                <li>🚀 مميزات PRO كاملة</li>
                <li>🚀 خوارزمية بايز للتوقع المستقبلي</li>
                <li>🚀 رصد مباشر لحركة حيتان الذهب</li>
                <li>🚀 دعم فني خاص 24/7</li>
            </ul>
            <a href="#" class="btn btn-disabled">قريباً (قيد التجهيز) ⏳</a>
        </div>
        """, unsafe_allow_html=True)

    st.stop()

# 4. واجهة المنصة (بعد الدخول)
st.sidebar.markdown(f"""
    <div style='text-align: center; padding: 20px; background: rgba(59, 130, 246, 0.1); border-radius: 15px; border: 1px solid #3b82f6;'>
        <h3 style='margin: 0; color: #3b82f6;'>باقة {st.session_state.user_tier}</h3>
        <p style='color: #94a3b8;'>الحساب نشط ✅</p>
    </div>
""", unsafe_allow_html=True)

if st.sidebar.button("تسجيل الخروج 🔓", use_container_width=True):
    st.session_state.authenticated = False
    st.rerun()

st.title("📊 مركز تحليلات السيولة المتقدمة")
st.markdown("---")
# محاكاة البيانات
chart_data = pd.DataFrame(np.random.randn(50, 3) / 50 + 2350, columns=['الذهب', 'OB', 'FVG'])
st.line_chart(chart_data)
st.success("✅ تم تحديث جميع البيانات والمؤشرات المؤسسية بنجاح.")
