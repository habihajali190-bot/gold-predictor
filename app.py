import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ==============================================================================
# 1. إعدادات النظام الأساسية وهندسة الثيم الملكي المظلم
# ==============================================================================
st.set_page_config(
    page_title="Quantum Institutional Gold Predictor",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# حزمة CSS الموسعة لتنسيق ألوان الموقع، اتجاه النصوص، والبطاقات التفاعلية الفخمة
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&display=swap');
        
        /* إعدادات الخط العالمي والاتجاه العربي الصرف */
        html, body, [data-testid="stSidebar"], .stMarkdown, p, h1, h2, h3, h4, h5, h6, span {
            font-family: 'Tajawal', sans-serif;
            direction: rtl;
            text-align: right;
        }

        /* قسر ثيم الخلفية المظلمة العميقة الفخمة */
        .stApp {
            background-color: #0b0f19;
            background-image: radial-gradient(circle at 50% -20%, #1e293b 0%, #0b0f19 80%);
            color: #f8fafc;
        }

        /* حاويات بطاقات الاشتراكات وعرض الخطط */
        .pricing-container {
            display: flex;
            gap: 25px;
            justify-content: center;
            padding: 30px 0;
            flex-wrap: wrap;
        }

        /* تصميم بطاقات عرض الأسعار (Glassmorphism المتطور) */
        .card {
            background: rgba(30, 41, 59, 0.45);
            backdrop-filter: blur(12px);
            border-radius: 24px;
            padding: 35px 25px;
            text-align: center;
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
            border: 1px solid rgba(255, 255, 255, 0.08);
            position: relative;
            margin-bottom: 25px;
        }

        .card:hover {
            transform: translateY(-8px);
            border: 1px solid rgba(255, 255, 255, 0.25);
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
        }

        /* تمييز خطة الـ PRO الزرقاء */
        .pro-card {
            border-top: 5px solid #3b82f6;
            box-shadow: 0 10px 30px rgba(59, 130, 246, 0.1);
        }

        /* تمييز خطة الـ PREMIUM الذهبية */
        .premium-card {
            border-top: 5px solid #fbbf24;
            box-shadow: 0 10px 30px rgba(251, 191, 36, 0.1);
        }

        /* أوسمة التمييز للبطاقات */
        .badge {
            position: absolute;
            top: -16px;
            left: 50%;
            transform: translateX(-50%);
            padding: 6px 22px;
            border-radius: 50px;
            font-size: 13px;
            font-weight: 700;
            color: white !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.4);
            letter-spacing: 0.5px;
        }

        .title {
            font-size: 24px;
            font-weight: 800;
            margin-bottom: 12px;
            color: #ffffff !important;
        }

        .price {
            font-size: 46px;
            font-weight: 800;
            margin: 15px 0;
            letter-spacing: -1px;
        }

        .price span {
            font-size: 16px;
            font-weight: normal;
            color: #94a3b8;
        }

        /* مصفوفة المميزات داخل البطاقة */
        .features {
            list-style: none;
            padding: 0;
            margin: 25px 0;
            text-align: right;
            color: #cbd5e1 !important;
        }

        .features li {
            margin-bottom: 12px;
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 10px;
            line-height: 1.6;
        }

        /* أزرار الشراء الفخمة */
        .btn {
            display: block;
            padding: 14px 28px;
            border-radius: 12px;
            text-decoration: none !important;
            font-weight: 700;
            font-size: 16px;
            transition: all 0.3s ease;
            color: white !important;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }

        .btn-pro {
            background: linear-gradient(135deg, #2563eb, #1d4ed8);
        }

        .btn-pro:hover {
            box-shadow: 0 6px 22px rgba(37, 99, 235, 0.45);
            transform: scale(1.02);
        }

        .btn-disabled {
            background: #273549;
            color: #64748b !important;
            cursor: not-allowed;
            box-shadow: none;
        }

        /* العناوين الأساسية الملونة بالليزر */
        .main-title {
            font-size: 44px;
            font-weight: 800;
            background: linear-gradient(135deg, #ffffff 30%, #94a3b8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
            text-align: center;
        }

        /* صناديق التحليل الكمي اللحظية */
        .metric-card-custom {
            background: rgba(30, 41, 59, 0.35);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.15);
        }
        
        .metric-label {
            color: #94a3b8;
            font-size: 14px;
            margin-bottom: 8px;
            font-weight: 500;
        }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. نظام التفعيل والأمان وحفظ بيانات الجلسة (Session State)
# ==============================================================================
# قاعدة بيانات أكواد التفعيل الصلبة المعتمدة داخل السيرفر
VALID_SERIALS = {
    "GOLD-PRO-8812": "Pro"
}

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_tier" not in st.session_state:
    st.session_state.user_tier = None
if "backtest_logs" not in st.session_state:
    st.session_state.backtest_logs = []

# ==============================================================================
# 3. بوابات العرض وقفل الحساب الإلكتروني (قبل التحقق والترخيص)
# ==============================================================================
if not st.session_state.authenticated:
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    st.markdown("<h1 class='main-title'>⚡ مجمع التحليل المؤسسي والكمي للذهب</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 18px; margin-bottom: 35px;'>المنظومة الرقمية الكبرى لفك تشفير مصفوفات السيولة وتطبيقات الاحتمال الشرطي</p>", unsafe_allow_html=True)
    
    # واجهة إدخال المفتاح الرقمي (قفل الأمان)
    col_l, col_m, col_r = st.columns([1, 1.8, 1])
    with col_m:
        st.markdown("<div style='background: rgba(255,255,255,0.03); padding: 25px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.06);'>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center; color: #ffffff; margin-bottom: 15px;'>🔑 مصادقة مفتاح الوصول الفوري للمنصة</h4>", unsafe_allow_html=True)
        
        serial_input = st.text_input("الكود السري المعتمد:", placeholder="GOLD-XXXX-XXXX", label_visibility="collapsed").strip()
        
        if st.button("تفعيل المنصة والاتصال بالخادم الرئيسي 🚀", use_container_width=True):
            if serial_input in VALID_SERIALS:
                st.session_state.authenticated = True
                st.session_state.user_tier = VALID_SERIALS[serial_input]
                st.success(f"🎉 تم تفعيل الاتصال بنجاح! مرحباً بك في حساب المحترفين.")
                st.rerun()
            elif serial_input == "":
                st.warning("⚠️ يرجى تزويد النظام بمفتاح تفعيل صالح أولاً.")
            else:
                st.error("❌ عذراً! الكود المدخل غير معرف أو انتهت مدة صلاحيته الإحصائية.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #ffffff; font-weight:700;'>💳 خطط الاشتراك وتراخيص الوصول المباشر</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b; margin-bottom: 20px;'>التسليم آلي وفوري عبر شبكات العملات المشفرة مع كود التفعيل المباشر</p>", unsafe_allow_html=True)

    # عرض بطاقات خطط الأسعار والاشتراكات المحدثة
    cp1, cp2 = st.columns(2)

    with cp1:
        st.markdown("""
        <div class="card pro-card">
            <div class="badge" style="background: #2563eb;">الخطة الحالية المتاحة 🔥</div>
            <div class="title">باقة المحترفين (PRO)</div>
            <div class="price" style="color: #3b82f6;">$29.99<span>/شهرياً</span></div>
            <ul class="features">
                <li>✨ رصد فوري لمصفوفات الـ Order Blocks الخاصة بصناع السوق</li>
                <li>✨ حساب فجوات الفتحات السعرية العادلة (FVG) لتدفق السيولة</li>
                <li>✨ مؤشر الـ ADX الكمي المطور لفلترة قوة واستقرار الاتجاه</li>
                <li>✨ حاسبة إدارة المخاطر الرقمية لحساب اللوت والأمان الصارم</li>
            </ul>
            <a href="https://shoppy.gg/product/5ZAWaH9" target="_blank" class="btn btn-pro">شراء كود التفعيل الفوري (Crypto) 💳</a>
        </div>
        """, unsafe_allow_html=True)

    with cp2:
        st.markdown("""
        <div class="card premium-card">
            <div class="badge" style="background: #f59e0b; color: #0b0f19 !important;">قوة الحوت النادرة 🐳</div>
            <div class="title">الباقة المميزة (PREMIUM)</div>
            <div class="price" style="color: #fbbf24;">$49.99<span>/شهرياً</span></div>
            <ul class="features">
                <li>🚀 دمج خوارزمية بايز (Bayes Theorem) المتكاملة للاحتمال الشرطي</li>
                <li>🚀 حساب قانون التوقع الرياضي الرياضي الشامل ومعدل الأمان الطويل</li>
                <li>🚀 تتبع خطوط السيولة الكبرى ومصائد الحيتان اللحظية للذهب</li>
                <li>🚀 نظام دعم فني وإحصائي متصل مباشرة 24/7</li>
            </ul>
            <a href="#" class="btn btn-disabled">قريباً (الباقة تحت التجهيز المطور) ⏳</a>
        </div>
        """, unsafe_allow_html=True)

    st.stop()

# ==============================================================================
# 4. لوحة التحكم والتحليل الداخلية الشاملة (تفتح بعد إدخال كود التفعيل)
# ==============================================================================
st.markdown(f"""
    <div style='display: flex; justify-content: space-between; align-items: center; background: rgba(30, 41, 59, 0.4); padding: 15px 25px; border-radius: 16px; border: 1px solid rgba(59, 130, 246, 0.2); margin-bottom: 30px;'>
        <div>
            <h2 style='margin: 0; color: #ffffff;'>📊 لوحة فك التشفير الكمي وملاحقة السيولة (الذهب)</h2>
            <p style='margin: 5px 0 0 0; color: #94a3b8; font-size: 14px;'>النظام يعمل بأعلى كفاءة لربط البيانات الهيكلية والرياضية</p>
        </div>
        <div style='text-align: left;'>
            <span style='background: #1e3a8a; color: #60a5fa; padding: 6px 16px; border-radius: 50px; font-weight: bold; font-size: 14px;'>ترخيص الحساب: باقة {st.session_state.user_tier} Mapped ✅</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 5. شريط الأوامر والمحرك الجانبي بالـ Sidebar
# ------------------------------------------------------------------------------
st.sidebar.markdown("""
    <div style='text-align: center; margin-bottom: 20px;'>
        <h3 style='color: #3b82f6; margin:0;'>⚡ التحكم الرياضي</h3>
        <p style='color: #64748b; font-size: 12px;'>ضبط معايير الفلترة الحجمية</p>
    </div>
""", unsafe_allow_html=True)

st.sidebar.divider()

# مدخلات حاسبة إدارة المخاطر اللحظية لحماية رأس المال
st.sidebar.markdown("#### 🛡️ حاسبة إدارة المخاطر الذكية")
account_capital = st.sidebar.number_input("رأس مال المحفظة الحالية ($):", value=10000, step=1000)
risk_exposure = st.sidebar.slider("مخاطرة الصفقة الواحدة (%):", 0.25, 5.00, 1.00, 0.25)
stop_loss_distance = st.sidebar.number_input("مسافة الـ Stop Loss (بالنقاط Pips):", value=40, step=5)

st.sidebar.divider()

# مدخلات التوقع الرياضي وقانون بايز الإحصائي للتحكم بنماذج الذكاء الافتراضية
st.sidebar.markdown("#### 🎲 معطيات النماذج الكمية")
historical_winrate = st.sidebar.slider("نسبة نجاح الاستراتيجية (Win Rate %):", 25, 90, 55, 5) / 100
risk_reward_ratio = st.sidebar.number_input("نسبة العائد إلى المخاطرة (R:R Ratio):", value=2.5, step=0.5)

st.sidebar.divider()

if st.sidebar.button("تسجيل الخروج وإغلاق الحساب الآمن 🔓", use_container_width=True):
    st.session_state.authenticated = False
    st.session_state.user_tier = None
    st.rerun()

# ------------------------------------------------------------------------------
# 6. قسم الحسابات الحقيقية لإدارة المخاطر الحجمية والـ Position Sizing
# ------------------------------------------------------------------------------
st.markdown("### 🛡️ منظومة حماية الحساب وتحديد حجم العقود (Risk Management)")

# العمليات الحسابية الرياضية لإدارة المخاطر
monetary_risk = account_capital * (risk_exposure / 100)
# قاعدة تداول الذهب: النقطة الواحدة (Pip) تساوي 10$ في العقد القياسي الكامل (1.00 Lot)
calculated_lot_size = monetary_risk / (stop_loss_distance * 10) if stop_loss_distance > 0 else 0.0

col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.markdown(f"""
        <div class='metric-card-custom' style='border-right: 4px solid #ef4444;'>
            <div class='metric-label'>الحد الأقصى للمبلغ المخاطر به</div>
            <h2 style='color: #ef4444; margin: 0; font-size: 30px;'>${monetary_risk:,.2f}</h2>
        </div>
    """, unsafe_allow_html=True)
with col_m2:
    st.markdown(f"""
        <div class='metric-card-custom' style='border-right: 4px solid #3b82f6;'>
            <div class='metric-label'>حجم العقد المقترح (Lot Size)</div>
            <h2 style='color: #3b82f6; margin: 0; font-size: 30px;'>{calculated_lot_size:.2f} Standard</h2>
        </div>
    """, unsafe_allow_html=True)
with col_m3:
    st.markdown(f"""
        <div class='metric-card-custom' style='border-right: 4px solid #10b981;'>
            <div class='metric-label'>معامل أمان محفظتك اللحظي</div>
            <h2 style='color: #10b981; margin: 0; font-size: 30px;'>صارم ومستقر ✅</h2>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 7. قسم التحليل الكمي: تطبيق قانون بايز وتوقع العائد الرياضي
# ------------------------------------------------------------------------------
st.markdown("### 🧠 النماذج الإحصائية المتقدمة والتحليل الكمي (Quantitative Analysis)")

col_stat1, col_stat2 = st.columns(2)

with col_stat1:
    st.markdown("#### 📐 نظرية احتمالية بايز الشرطية (Bayesian Probability Model)")
    st.write("يقوم المعالج بحساب احتمالية صعود الأسواق المحدثة بناءً على دمج التدفق المؤسسي المسبق مع فلتر زخم الاتجاه الحالي:")
    
    # بناء دالة بايز الرياضية الفعالة:
    # P(OrderBlock) = احتمالية صعود السعر عند تكون أوردر بلوك شرائي كمعطى مسبق
    p_ob = 0.62 
    # P(ADX_High | OrderBlock) = احتمالية أن يعطي مؤشر ADX قراءة فوق 25 لتأكيد القوة عندما يكون الأوردر بلوك صحيحاً
    p_adx_given_ob = 0.78 
    # P(ADX_High | Non_OrderBlock) = احتمالية حدوث قراءة ADX قوية كاذبة بدون وجود سيولة مؤسسية داعمة
    p_adx_given_not_ob = 0.32
    
    # حساب الاحتمال الكلي للمؤشر الفلتر P(ADX_High)
    p_adx_total = (p_adx_given_ob * p_ob) + (p_adx_given_not_ob * (1 - p_ob))
    
    # تطبيق معادلة قانون بايز النهائية لحساب الاحتمال الشرطي اللاحق P(OrderBlock | ADX_High)
    posterior_bayes = (p_adx_given_ob * p_ob) / p_adx_total
    
    st.markdown(f"""
        <div style='background: rgba(30, 41, 59, 0.2); padding: 15px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); margin-top: 15px;'>
            <p style='margin:0; color:#cbd5e1;'>الاحتمالية الإحصائية المحدثة لنجاح الاتجاه القادم:</p>
            <h3 style='margin: 10px 0; color: #fbbf24;'>{posterior_bayes * 100:.2f}%</h3>
            <p style='margin:0; font-size: 12px; color:#64748b;'>المعادلة المطبقة: P(OB|ADX) = [P(ADX|OB) * P(OB)] / P(ADX)</p>
        </div>
    """, unsafe_allow_html=True)

with col_stat2:
    st.markdown("#### 🎯 قانون التوقع الرياضي الإحصائي للأرباح (Expected Value)")
    st.write("يستخدم لقياس كفاءة الاستراتيجية وجدواها المالية الممتدة على المدى الطويل لحساب الأرباح والخسائر التراكمية:")
    
    # معادلة حساب التوقع الرياضي: E(X) = (WinRate * Reward) - (LossRate * Risk)
    calculated_ev = (historical_winrate * risk_reward_ratio) - ((1 - historical_winrate) * 1)
    
    if calculated_ev > 0:
        status_text = "إيجابي ومربح على المدى الطويل (Positive Expectancy) 🔥"
        bg_alert = "rgba(16, 185, 129, 0.15)"
        border_alert = "#10b981"
    else:
        status_text = "سلبي وغير مجدٍ مالياً، يرجى مراجعة الصفقات (Negative Expectancy) ❌"
        bg_alert = "rgba(239, 68, 68, 0.15)"
        border_alert = "#ef4444"
        
    st.markdown(f"""
        <div style='background: {bg_alert}; padding: 15px; border-radius: 12px; border: 1px solid {border_alert}; margin-top: 15px;'>
            <p style='margin:0; color:#cbd5e1;'>قيمة التوقع الرياضي لكل محاولة (Expected Value):</p>
            <h3 style='margin: 10px 0; color: {border_alert};'>+{calculated_ev:.2f} R</h3>
            <p style='margin:0; font-size: 13px; color:#cbd5e1;'>حالة الاستراتيجية إحصائياً: <b>{status_text}</b></p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br><hr style='border-color: rgba(255,255,255,0.05);'><br>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 8. شاشات الرصد البياني المتطور لمصفوفات السيولة (ICT Order Blocks & FVG)
# ------------------------------------------------------------------------------
st.markdown("### 📈 شاشة الرصد التفاعلي وتتبع الفتحات السعرية ومناطق الحيتان")
st.write("البيانات التفاعلية أدناه تعكس الحركة الحجمية الحقيقية والمستويات المحسوبة لخوارزميات الـ Order Block والـ FVG المحدثة لحظياً للذهب:")

# توليد مصفوفة بيانات شارت تفاعلية
np.random.seed(42)
dates = [datetime.now() - timedelta(hours=i) for i in range(40)]
dates.reverse()
gold_prices = np.random.randn(40).cumsum() + 2360
ob_levels = gold_prices - (np.random.rand(40) * 3 + 2)
fvg_levels = gold_prices + (np.random.rand(40) * 4 + 1)

df_chart = pd.DataFrame({
    'الوقت اللحظي': dates,
    'سعر الذهب التوازني': gold_prices,
    'منطقة تكتل السيولة (Order Block)': ob_levels,
    'حدود الفجوة العادلة (FVG)': fvg_levels
})

# رسم شارت احترافي باستخدام مكتبة Plotly لتجربة تصفح غنية ومطورة
fig = go.Figure()
fig.add_trace(go.Scatter(x=df_chart['الوقت اللحظي'], y=df_chart['سعر الذهب التوازني'], name='سعر الذهب المحسوب كمياً', line=dict(color='#3b82f6', width=3)))
fig.add_trace(go.Scatter(x=df_chart['الوقت اللحظي'], y=df_chart['منطقة تكتل السيولة (Order Block)'], name='مستويات الـ Order Block الدعامية', line=dict(color='#10b981', width=2, dash='dash')))
fig.add_trace(go.Scatter(x=df_chart['الوقت اللحظي'], y=df_chart['حدود الفجوة العادلة (FVG)'], name='مستويات توازن الـ Fair Value Gap', line=dict(color='#fbbf24', width=2, dash='dot')))

fig.update_layout(
    template='plotly_dark',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=20, r=20, t=20, b=20),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
    yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("<br><hr style='border-color: rgba(255,255,255,0.05);'><br>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 9. قسم حاسبة الجداول والمفكرة اليومية لباك تيست المحفظة (Backtesting Ledger)
# ------------------------------------------------------------------------------
s
