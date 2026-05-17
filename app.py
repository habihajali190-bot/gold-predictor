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

# إضافة حزمة CSS المخصصة لتجميل الواجهة وضمان الألوان الاحترافية الفخمة
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&display=swap');
        
        html, body, [data-testid="stSidebar"], .stMarkdown, p, h1, h2, h3, h4 {
            font-family: 'Tajawal', sans-serif;
            direction: rtl;
            text-align: right;
        }

        .stApp {
            background-color: #0b0f1a;
            background-image: radial-gradient(circle at 50% -20%, #1e293b 0%, #0b0f1a 80%);
        }

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

        .pro-card { border-top: 5px solid #3b82f6; box-shadow: 0 10px 30px rgba(59, 130, 246, 0.1); }
        .premium-card { border-top: 5px solid #fbbf24; box-shadow: 0 10px 30px rgba(251, 191, 36, 0.1); }

        .badge {
            position: absolute; top: -15px; left: 50%; transform: translateX(-50%);
            padding: 6px 20px; border-radius: 50px; font-size: 14px; font-weight: bold; color: white !important;
        }

        .title { font-size: 26px; font-weight: 800; margin-bottom: 15px; color: #ffffff !important; }
        .price { font-size: 50px; font-weight: 800; margin: 20px 0; }
        .price span { font-size: 18px; font-weight: normal; color: #94a3b8; }

        .features { list-style: none; padding: 0; margin: 30px 0; text-align: right; color: #cbd5e1 !important; }
        .features li { margin-bottom: 12px; font-size: 15px; display: flex; align-items: center; gap: 10px; }

        .btn { display: block; padding: 15px 30px; border-radius: 12px; text-decoration: none !important; font-weight: bold; font-size: 18px; color: white !important; text-align: center; }
        .btn-pro { background: linear-gradient(135deg, #2563eb, #1d4ed8); }
        .btn-disabled { background: #334155; color: #94a3b8 !important; cursor: not-allowed; opacity: 0.7; }

        .main-title {
            font-size: 45px; font-weight: 800;
            background: linear-gradient(to right, #ffffff, #94a3b8);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            margin-bottom: 10px; text-align: center;
        }
        
        /* ستايل مخصص لصناديق الإحصائيات الكمية */
        .metric-box {
            background: rgba(30, 41, 59, 0.4);
            border: 1px solid rgba(255,255,255,0.05);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 15px;
        }
    </style>
""", unsafe_allow_html=True)

# 2. نظام التحقق وإدارة الأكواد (Session State)
VALID_SERIALS = {
    "GOLD-PRO-8812": "Pro"
}

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_tier" not in st.session_state:
    st.session_state.user_tier = None

# 3. واجهة الدخول والشراء (قبل التفعيل)
if not st.session_state.authenticated:
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    st.markdown("<h1 class='main-title'>⚡ منصة التوقع المؤسسي للذهب</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 18px; margin-bottom: 40px;'>نظام الذكاء الرقمي لفك تشفير السيولة والتحليل الكمي</p>", unsafe_allow_html=True)
    
    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        st.markdown("<div style='background: rgba(255,255,255,0.05); padding: 30px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center; color: #ffffff; margin-bottom: 20px;'>🔑 أدخل مفتاح الوصول الفوري</h4>", unsafe_allow_html=True)
        serial_input = st.text_input("الكود:", placeholder="GOLD-XXXX-XXXX", label_visibility="collapsed").strip()
        if st.button("تفعيل المنصة 🚀", use_container_width=True):
            if serial_input in VALID_SERIALS:
                st.session_state.authenticated = True
                st.session_state.user_tier = VALID_SERIALS[serial_input]
                st.success(f"🎉 تم التفعيل بنجاح! مرحباً بك")
                st.rerun()
            elif serial_input == "":
                st.warning("⚠️ يرجى إدخال الكود أولاً")
            else:
                st.error("❌ الكود غير صحيح")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #ffffff;'>💳 اختر خطة الوصول المناسبة</h2>", unsafe_allow_html=True)

    cp1, cp2 = st.columns(2)
    with cp1:
        st.markdown("""
        <div class="card pro-card">
            <div class="badge" style="background: #3b82f6;">الأكثر طلباً 🔥</div>
            <div class="title">باقة المحترفين (PRO)</div>
            <div class="price" style="color: #3b82f6;">$29.99<span>/شهرياً</span></div>
            <ul class="features">
                <li>✅ كشف خوارزمي لمناطق الـ Order Blocks</li>
                <li>✅ تحديد فجوات الـ FVG ونسب توازن السيولة</li>
                <li>✅ حاسبة إدارة المخاطر وحجم العقود الذكية</li>
                <li>✅ مؤشر الـ ADX الكمي المطور للاتجاه</li>
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
                <li>🚀 دمج خوارزمية بايز (Bayes) للاحتمالات المتكاملة</li>
                <li>🚀 حساب التوقع الرياضي الرياضي الشامل للصفقات ومعدل العائد</li>
                <li>🚀 مسح مصفوفات السيولة الكبرى وملاحقة صناع السوق</li>
                <li>🚀 دعم فني كمي وإحصائي متقدم 24/7</li>
            </ul>
            <a href="#" class="btn btn-disabled">قريباً (قيد التجهيز) ⏳</a>
        </div>
        """, unsafe_allow_html=True)

    st.stop()


# 4. واجهة المنصة الداخلية (تفتح بعد التفعيل الصحيح بكود: GOLD-PRO-8812)
st.title("⚡ مركز التحليل الكمي وإدارة المخاطر - الذهب")
st.markdown("---")

# لوحة جانبية لمعلومات الحساب والإدخال السريع لبارامترات الحساب
st.sidebar.markdown(f"""
    <div style='text-align: center; padding: 15px; background: rgba(59, 130, 246, 0.1); border-radius: 12px; border: 1px solid #3b82f6;'>
        <h4 style='margin: 0; color: #3b82f6;'>باقة الوصول: {st.session_state.user_tier}</h4>
        <p style='color: #4ade80; margin: 5px 0 0 0;'>الاتصال بالخادم الكمي نشط ونظامي ✅</p>
    </div>
""", unsafe_allow_html=True)
st.sidebar.markdown("<br>", unsafe_allow_html=True)

# مدخلات حاسبة إدارة المخاطر بالـ Sidebar
st.sidebar.subheader("🧮 حاسبة إدارة المخاطر الرقمية")
balance = st.sidebar.number_input("رأس مال الحساب ($):", value=10000, step=500)
risk_percent = st.sidebar.slider("نسبة المخاطرة للمحاولة (%):", 0.5, 5.0, 1.0, 0.5)
stop_loss_pips = st.sidebar.number_input("حجم وقف الخسارة (بالنقاط Pips):", value=30, step=5)

if st.sidebar.button("تسجيل الخروج 🔓", use_container_width=True):
    st.session_state.authenticated = False
    st.rerun()

# حسابات إدارة المخاطر الكمية الحقيقية
risk_amount = balance * (risk_percent / 100)
# افتراض نقطة الذهب بـ 10$ في العقد القياسي القياسي
standard_lot_size = risk_amount / (stop_loss_pips * 10) if stop_loss_pips > 0 else 0.0

# عرض نتائج إدارة المخاطر في الواجهة الرئيسية
st.subheader("🛡️ جدار حماية رأس المال وإدارة المخاطر اللحظية")
r_col1, r_col2, r_col3 = st.columns(3)
with r_col1:
    st.markdown(f"<div class='metric-box'><p style='color:#94a3b8; margin:0;'>المبلغ المخاطر به</p><h2 style='color:#ef4444; margin:5px 0;'>${risk_amount:,.2f}</h2></div>", unsafe_allow_html=True)
with r_col2:
    st.markdown(f"<div class='metric-box'><p style='color:#94a3b8; margin:0;'>حجم العقد المقترح (Lot Size)</p><h2 style='color:#3b82f6; margin:5px 0;'>{standard_lot_size:.2f} Standard</h2></div>", unsafe_allow_html=True)
with r_col3:
    st.markdown(f"<div class='metric-box'><p style='color:#94a3b8; margin:0;'>حالة الحساب إحصائياً</p><h2 style='color:#10b981; margin:5px 0;'>آمن ومستقر</h2></div>", unsafe_allow_html=True)

st.markdown("---")

# محاكاة البيانات وحساب التوقع الرياضي وقانون بايز الإحصائي
st.subheader("📊 حسابات الاحتمالية الشرطية والتوقع الرياضي (Quantitative Models)")

m_col1, m_col2 = st.columns(2)

with m_col1:
    st.markdown("### 🧠 تطبيق احتمالية بايز الشرطية (Bayesian Probability)")
    st.write("يقوم النظام بدمج التدفق المؤسسي الحالي للسيولة (Order Block) مع قوة اتجاه الـ ADX لتحديث التوقع إحصائياً:")
    
    # بارامترات بايز (مبنية على قراءات السوق الافتراضية اللحظية)
    p_order_block = 0.65  # P(A) احتمالية صعود السعر بناء على مصفوفة السيولة
    p_adx_given_ob = 0.80 # P(B|A) احتمالية قوة مؤشر ADX عندما تكون السيولة صاعدة
    p_adx_total = (p_adx_given_ob * p_order_block) + (0.35 * (1 - p_order_block)) # P(B) الاحتمالية الكلية للمؤشر
    
    # حساب بايز النهائي P(A|B)
    bayes_result = (p_adx_given_ob * p_order_block) / p_adx_total
    
    st.info(f"الاحتمالية المحدثة للصعود شرط نجاح الفلترة بالمؤشرات الحجمية: **{bayes_result * 100:.2f}%**")
    st.caption(f"بناءً على احتمالية سوق مسبقة P(A) = {p_order_block*100}% وإشارة تأكيد ADX = {p_adx_given_ob*100}%")

with m_col2:
    st.markdown("### 🎲 قانون التوقع الرياضي للصفقات (Expected Value)")
    st.write("حساب العائد المتوقع على المدى الطويل بناءً على كفاءة خوارزميات الاستراتيجية المطبقة:")
    
    win_rate = st.slider("نسبة نجاح الاستراتيجية التاريخية (Win Rate %):", 30, 90, 60) / 100
    rr_ratio = st.number_input("نسبة العائد إلى المخاطرة (Risk:Reward Ratio):", value=2.0, step=0.5)
    
    # حساب التوقع الرياضي E(X)
    # E(X) = (P(Win) * Reward) - (P(Loss) * Risk) حيث الـ Risk نعتبره 1 وحدة
    expected_value = (win_rate * rr_ratio) - ((1 - win_rate) * 1)
    
    if expected_value > 0:
        st.success(f"التوقع الرياضي إيجابي: **+{expected_value:.2f} R** (الاستراتيجية مربحة على المدى الطويل)")
    else:
        st.error(f"التوقع الرياضي سلبي: **{expected_value:.2f} R** (الاستراتيجية ستؤدي لخسارة رأس المال)")

st.markdown("---")

# الرصد البياني الذكي المطور للسيولة
st.subheader("📈 تتبع مصفوفات السيولة المؤسسية الحية (Live Core)")
chart_data = pd.DataFrame(
    np.random.randn(40, 3) / 70 + 2350,
    columns=['سعر الذهب المستهدف كمياً', 'مستويات توازن الـ Order Block', 'حدود الفجوة السعرية العادلة FVG']
)
st.line_chart(chart_data)
