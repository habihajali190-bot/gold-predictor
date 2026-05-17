import streamlit as st
import pandas as pd
import numpy as np

# 1. إعدادات الصفحة الأساسية وتحسين الثيم العام
st.set_page_config(
    page_title="Quantum Institutional Bayesian Predictor",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# إضافة حزمة CSS مخصصة لتجميل الواجهة والخلفيات بالكامل
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap');
        
        /* ضبط الخط العام للموقع */
        html, body, [data-testid="stSidebar"], .stMarkdown {
            font-family: 'Tajawal', sans-serif;
            direction: rtl;
            text-align: right;
        }
        
        /* تجميل بطاقات الأسعار */
        .pricing-container {
            display: flex;
            gap: 20px;
            justify-content: center;
            flex-wrap: wrap;
            margin-top: 30px;
        }
        
        .pricing-card {
            background: linear-gradient(145deg, #1e293b, #0f172a);
            border-radius: 16px;
            padding: 30px;
            text-align: center;
            position: relative;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            width: 100%;
            max-width: 400px;
        }
        
        .pricing-card.pro {
            border: 2px solid #3b82f6;
            box-shadow: 0 10px 25px rgba(59, 130, 246, 0.15);
        }
        
        .pricing-card.premium {
            border: 1px solid #475569;
            opacity: 0.8;
        }
        
        .pricing-card:hover {
            transform: translateY(-5px);
        }
        
        .pricing-card.pro:hover {
            box-shadow: 0 15px 35px rgba(59, 130, 246, 0.3);
        }
        
        .badge {
            background: linear-gradient(90deg, #3b82f6, #1d4ed8);
            color: white;
            padding: 6px 16px;
            border-radius: 50px;
            font-size: 13px;
            font-weight: bold;
            position: absolute;
            top: -15px;
            left: 50%;
            transform: translateX(-50%);
            box-shadow: 0 4px 10px rgba(59, 130, 246, 0.4);
        }
        
        .plan-title {
            color: #f8fafc;
            font-size: 24px;
            font-weight: 700;
            margin-top: 10px;
        }
        
        .plan-price {
            font-size: 42px;
            font-weight: 800;
            color: #3b82f6;
            margin: 20px 0;
        }
        
        .plan-price span {
            font-size: 16px;
            color: #94a3b8;
            font-weight: normal;
        }
        
        .features-list {
            list-style: none;
            padding: 0;
            margin: 0 0 30px 0;
            text-align: right;
        }
        
        .features-list li {
            color: #cbd5e1;
            font-size: 15px;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        /* تجميل زر الشراء الخاص بـ Shoppy */
        .buy-button-pro {
            background: linear-gradient(90deg, #2563eb, #1d4ed8);
            color: white !important;
            padding: 14px 28px;
            border-radius: 10px;
            text-decoration: none !important;
            display: block;
            font-weight: bold;
            font-size: 16px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
        }
        
        .buy-button-pro:hover {
            background: linear-gradient(90deg, #1d4ed8, #1e40af);
            box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4);
            transform: scale(1.02);
        }
        
        .buy-button-disabled {
            background: #334155;
            color: #94a3b8 !important;
            padding: 14px 28px;
            border-radius: 10px;
            text-decoration: none !important;
            display: block;
            font-weight: bold;
            font-size: 16px;
            cursor: not-allowed;
        }
    </style>
""", unsafe_allow_html=True)

# 2. نظام التحقق وإدارة أكواد التفعيل
VALID_SERIALS = {
    "GOLD-PRO-8812": "Pro"
}

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_tier" not in st.session_state:
    st.session_state.user_tier = None

# 3. واجهة التفعيل وقفل المنصة الذكي
if not st.session_state.authenticated:
    # رأس الصفحة بتصميم أنيق
    st.markdown("""
        <div style='text-align: center; padding: 20px 0;'>
            <h1 style='color: #f8fafc; font-size: 38px; font-weight: 800;'>⚡ منصة التوقع المؤسسي الذكي للذهب</h1>
            <p style='color: #94a3b8; font-size: 16px; max-width: 700px; margin: 10px auto;'>
                مرحباً بك في النظام الرقمي المتقدم لفك تشفير السيولة وتتبع صناع السوق بناءً على خوارزميات الفتحات السعرية العادلة والمؤشرات الحجمية المتطورة.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.団 = st.container()
    with st.団:
        col_input, col_btn = st.columns([3, 1])
        with col_input:
            serial_input = st.text_input("مفتاح التفعيل الفوري:", placeholder="GOLD-XXXX-XXXX", label_visibility="collapsed").strip()
        with col_btn:
            activate_clicked = st.button("تفعيل المنصة 🚀", use_container_width=True)
            
        if activate_clicked:
            if serial_input in VALID_SERIALS:
                st.session_state.authenticated = True
                st.session_state.user_tier = VALID_SERIALS[serial_input]
                st.success(f"🎉 تم التفعيل بنجاح! مرحباً بك في الباقة ({st.session_state.user_tier})")
                st.rerun()
            elif serial_input == "":
                st.warning("⚠️ الرجاء إدخال كود التفعيل أولاً.")
            else:
                st.error("❌ كود التفعيل الذي أدخلته غير صحيح أو منتهي الصلاحية.")

    st.markdown("<br><hr style='border-color: #334155;'><br>", unsafe_allow_html=True)

    # قسم خطط الاشتراك وعرض البطاقات الاحترافية الجديدة
    st.markdown("<h2 style='text-align: center; color: #f8fafc;'>💳 خطط الاشتراك المتاحة للوصول الفوري</h2>", unsafe_allow_html=True)
    
    col_p1, col_p2 = st.columns(2)
    
    with col_p1:
        st.markdown("""
        <div class="pricing-card pro">
            <div class="badge">الأكثر طلباً وفائدة 🔥</div>
            <div class="plan-title">باقة المحترفين (PRO)</div>
            <div class="plan-price">$29.99<span>/شهرياً</span></div>
            <ul class="features-list">
                <li>🎯 كشف دقيق لمناطق الـ Order Blocks المؤسسية</li>
                <li>⚡ تحديد الفجوات السعرية العادلة (FVG) بدقة عالية</li>
                <li>📊 مؤشر الـ ADX المطور لقياس قوة زخم الاتجاه</li>
                <li>🔔 تنبيهات لحظية وتحديثات تلقائية للسيولة</li>
            </ul>
            <a href="https://shoppy.gg/product/5ZAWaH9" target="_blank" class="buy-button-pro">شراء كود التفعيل الفوري (Crypto) 💳</a>
        </div>
        """, unsafe_allow_html=True)

    with col_p2:
        st.markdown("""
        <div class="pricing-card premium">
            <div class="plan-title">الباقة المميزة (PREMIUM)</div>
            <div class="plan-price">$59.99<span>/شهرياً</span></div>
            <ul class="features-list">
                <li>🚀 جميع مميزات باقة PRO المحترفة الكاملة</li>
                <li>🧠 دمج معادلة بايز الإحصائية لاحتمالات السيولة المتكاملة</li>
                <li>📈 تحليلات يومية مخصصة لحركة الحيتان وصناع السوق</li>
                <li>📞 خط دعم فني مباشر وخاص على مدار الساعة 24/7</li>
            </ul>
            <a href="#" class="buy-button-disabled">قريباً (قيد التجهيز) ⏳</a>
        </div>
        """, unsafe_allow_html=True)

    st.stop()

# 4. واجهة المنصة الداخلية (تفتح بعد إدخال الكود الصحيح)
st.sidebar.markdown(f"""
    <div style='text-align: center; padding: 15px; background: #1e293b; border-radius: 12px; border: 1px solid #3b82f6;'>
        <h4 style='margin: 0; color: #94a3b8;'>نوع الاشتراك الحالي</h4>
        <h2 style='margin: 5px 0 0 0; color: #3b82f6;'>باقة {st.session_state.user_tier}</h2>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<br>", unsafe_allow_html=True)
if st.sidebar.button("تسجيل الخروج وإغلاق الحساب 🔓", use_container_width=True):
    st.session_state.authenticated = False
    st.session_state.user_tier = None
    st.rerun()

# محتوى لوحة التحكم الاحترافية للمشترك
st.title("📊 لوحة فك تشفير السيولة المتقدمة للذهب")
st.markdown("---")

# توليد بيانات حية متناسقة لمحاكاة الشارتات
chart_data = pd.DataFrame(
    np.random.randn(30, 3) / 60 + 2350,
    columns=['سعر الذهب الحالي', 'مناطق الـ Order Block', 'مستويات الـ FVG']
)

st.subheader("📈 الرصد البياني المباشر لحركة تدفقات السيولة")
st.line_chart(chart_data)

st.success("✅ اتصال بخوادم البيانات آمن والمؤشرات تعمل بأعلى كفاءة وفقاً للاتجاه.")
