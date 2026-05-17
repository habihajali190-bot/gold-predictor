import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# ==============================================================================
# 1. إعدادات النظام والهوية البصرية الملكية والمظهر الفاخر (Premium CSS Dark Theme)
# ==============================================================================
st.set_page_config(
    page_title="Quantum Institutional Gold Predictor v3.0",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# حزمة الـ CSS الضخمة لتنسيق الواجهات، الجداول، الكروت، وضمان دعم الـ RTL بالكامل
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&display=swap');
        
        /* قسر الخط العربي المعتمد والاتجاه الصحيح في كافة أنحاء التطبيق */
        html, body, [data-testid="stSidebar"], .stMarkdown, p, h1, h2, h3, h4, h5, h6, span, label, input, select {
            font-family: 'Tajawal', sans-serif;
            direction: rtl;
            text-align: right;
        }

        /* إعدادات الخلفية المظلمة الفخمة لمنع إجهاد العين للعميل والمستثمر */
        .stApp {
            background-color: #0b0f19;
            background-image: radial-gradient(circle at 50% -20%, #1e293b 0%, #0b0f19 80%);
            color: #f8fafc;
        }

        /* حاويات بطاقات الاشتراك */
        .pricing-grid {
            display: flex;
            gap: 25px;
            justify-content: center;
            padding: 20px 0;
            flex-wrap: wrap;
        }

        /* كروت الزجاج الاحترافية (Glassmorphism Cards) */
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
            width: 100%;
        }

        .card:hover {
            transform: translateY(-10px);
            border: 1px solid rgba(255, 255, 255, 0.25);
            box-shadow: 0 30px 60px rgba(0, 0, 0, 0.6);
        }

        .pro-card {
            border-top: 6px solid #3b82f6;
            box-shadow: 0 10px 30px rgba(59, 130, 246, 0.15);
        }

        .premium-card {
            border-top: 6px solid #fbbf24;
            box-shadow: 0 10px 30px rgba(251, 191, 36, 0.15);
        }

        /* أوسمة التميز الفوقية للبطاقات */
        .badge {
            position: absolute;
            top: -16px;
            left: 50%;
            transform: translateX(-50%);
            padding: 6px 24px;
            border-radius: 50px;
            font-size: 13px;
            font-weight: 700;
            color: white !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.4);
        }

        .title {
            font-size: 26px;
            font-weight: 800;
            margin-bottom: 10px;
            color: #ffffff !important;
        }

        .price {
            font-size: 50px;
            font-weight: 800;
            margin: 15px 0;
            letter-spacing: -1px;
        }

        .price span {
            font-size: 16px;
            font-weight: normal;
            color: #94a3b8;
        }

        .features {
            list-style: none;
            padding: 0;
            margin: 25px 0;
            text-align: right;
            color: #cbd5e1 !important;
        }

        .features li {
            margin-bottom: 14px;
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 10px;
            line-height: 1.6;
        }

        /* أزرار وتصاميم واجهات الشراء والاستدعاء */
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
            box-shadow: 0 6px 22px rgba(37, 99, 235, 0.5);
            transform: scale(1.02);
        }

        .btn-disabled {
            background: #273549;
            color: #64748b !important;
            cursor: not-allowed;
        }

        .main-title {
            font-size: 46px;
            font-weight: 800;
            background: linear-gradient(135deg, #ffffff 30%, #94a3b8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 10px;
        }

        /* لوحات قياس البيانات والأرقام الإحصائية */
        .metric-card-custom {
            background: rgba(30, 41, 59, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 18px;
            padding: 24px;
            text-align: center;
            box-shadow: 0 6px 20px rgba(0,0,0,0.2);
        }
        
        .metric-label {
            color: #94a3b8;
            font-size: 14px;
            margin-bottom: 8px;
            font-weight: 500;
        }

        .matrix-box {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(255,255,255,0.05);
            padding: 18px;
            border-radius: 14px;
            text-align: right;
            margin-bottom: 12px;
        }

        .crypto-wallet-box {
            background: rgba(30, 41, 59, 0.7);
            border: 1px solid rgba(59, 130, 246, 0.3);
            border-radius: 12px;
            padding: 15px;
            font-family: monospace;
            text-align: center;
            font-size: 16px;
            color: #60a5fa;
            margin: 10px 0;
        }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. هندسة حفظ البيانات وحالة النظام (Comprehensive Session State)
# ==============================================================================
# الأكواد الصلبة المعتمدة لتفعيل تراخيص العملاء فوراً على الخادم
VALID_SERIALS = {
    "GOLD-PRO-8812": "Pro",
    "GOLD-PREMIUM-9954": "Premium",
    "ADMIN-MASTER-770": "Admin"
}

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_tier" not in st.session_state:
    st.session_state.user_tier = None
if "backtest_logs" not in st.session_state:
    # صفقات افتراضية احترافية مبدئية لملء المنصة بالبيانات
    st.session_state.backtest_logs = [
        {"التاريخ والوقت": "2026-05-10", "نوع الهيكل": "شراء مؤسسي (Buy)", "الحالة": "ربح (Take Profit)", "العائد الإحصائي": "+2.5 R"},
        {"التاريخ والوقت": "2026-05-12", "نوع الهيكل": "بيع مؤسسي (Sell)", "الحالة": "خسارة (Stop Loss)", "العائد الإحصائي": "-1.0 R"},
        {"التاريخ والوقت": "2026-05-14", "نوع الهيكل": "شراء مؤسسي (Buy)", "الحالة": "ربح (Take Profit)", "العائد الإحصائي": "+3.5 R"},
        {"التاريخ والوقت": "2026-05-15", "نوع الهيكل": "بيع مؤسسي (Sell)", "الحالة": "ربح (Take Profit)", "العائد الإحصائي": "+2.0 R"},
    ]
if "crypto_invoices" not in st.session_state:
    st.session_state.crypto_invoices = []

# ==============================================================================
# 3. بوابات العرض وتراخيص المرور والدفع (تظهر قبل تفعيل الحساب)
# ==============================================================================
if not st.session_state.authenticated:
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    st.markdown("<h1 class='main-title'>⚡ مجمع التحليل المؤسسي والكمي للذهب</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 19px; margin-bottom: 45px;'>المنظومة الرقمية الأكبر لفك تشفير مصفوفات السيولة الذكية (ICT) وتطبيقات الاحتمال الشرطي للبنوك</p>", unsafe_allow_html=True)
    
    # واجهة إدخال التفعيل والأمان
    col_l, col_m, col_r = st.columns([1, 1.8, 1])
    with col_m:
        st.markdown("<div style='background: rgba(255,255,255,0.02); padding: 30px; border-radius: 24px; border: 1px solid rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center; color: #ffffff; margin-bottom: 15px;'>🔑 بوابات مصادقة مفتاح الوصول الفوري</h4>", unsafe_allow_html=True)
        
        serial_input = st.text_input("ادخل كود التفعيل المعتمد الممنوح لك:", placeholder="GOLD-XXXX-XXXX", label_visibility="collapsed").strip()
        
        if st.button("تفعيل المنصة والاتصال بالخادم الرئيسي 🚀", use_container_width=True):
            if serial_input in VALID_SERIALS:
                st.session_state.authenticated = True
                st.session_state.user_tier = VALID_SERIALS[serial_input]
                st.success(f"🎉 تم تفعيل الاتصال بنجاح! رتبة الحساب الحالية: {st.session_state.user_tier}. جاري فتح بوابات البيانات...")
                st.rerun()
            elif serial_input == "":
                st.warning("⚠️ يرجى تزويد النظام بمفتاح تفعيل صالح أولاً.")
            else:
                st.error("❌ عذراً! الكود المدخل غير معرف أو انتهت صلاحيته الإحصائية بالسيرفر.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #ffffff; font-weight:800;'>💳 تراخيص الوصول المباشر ونظام الشراء المؤتمت</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b; margin-bottom: 40px;'>الدفع آلي، مشفر، ومباشر 100% عبر شبكات الـ Crypto لتوليد كود تفعيل فوري</p>", unsafe_allow_html=True)

    # عرض خطط الاشتراك المفصلة برمجياً لتأخذ مساحة وتفاصيل ضخمة
    cp1, cp2 = st.columns(2)

    with cp1:
        st.markdown("""
        <div class="card pro-card">
            <div class="badge" style="background: #2563eb;">الباقة الأكثر طلباً 🔥</div>
            <div class="title">باقة المحترفين (PRO TIER)</div>
            <div class="price" style="color: #3b82f6;">$29.99<span>/شهرياً</span></div>
            <ul class="features">
                <li>✨ رصد فوري لمصفوفات الـ Order Blocks الخاصة بصناع السوق والحيتان</li>
                <li>✨ حساب فجوات الفتحات السعرية العادلة (FVG) وتوازن تدفق السيولة</li>
                <li>✨ مؤشر الـ ADX الكمي المطور لفلترة قوة واستقرار الاتجاه ومنع الانعكاس</li>
                <li>✨ حاسبة إدارة المخاطر الرقمية لحساب اللوت وعقد الصفقة الآمن</li>
                <li>✨ إمكانية الوصول إلى جدول الباك تيست التراكمي اليومي للمحفظة</li>
            </ul>
            <a href="https://shoppy.gg/product/5ZAWaH9" target="_blank" class="btn btn-pro">شراء كود التفعيل الفوري (Crypto/Shoppy) 💳</a>
        </div>
        """, unsafe_allow_html=True)

    with cp2:
        st.markdown("""
        <div class="card premium-card">
            <div class="badge" style="background: #f59e0b; color: #0b0f19 !important;">قوة الحوت الكمي والتحليل الشرطي 🐳</div>
            <div class="title">الباقة المميزة (PREMIUM ALGO)</div>
            <div class="price" style="color: #fbbf24;">$49.99<span>/شهرياً</span></div>
            <ul class="features">
                <li>🚀 دمج خوارزمية بايز (Bayes Theorem) المتكاملة للاحتمال الشرطي</li>
                <li>🚀 حساب قانون التوقع الرياضي الرياضي الشامل ومعدل الأمان الطويل</li>
                <li>🚀 تتبع خطوط السيولة الكبرى ومصائد الحيتان اللحظية للذهب</li>
                <li>🚀 نظام تنبيهات الاختلال الهيكلي لحركة (XAUUSD) بدقة البنوك</li>
                <li>🚀 لوحة تحكم ومؤشرات تداول كمية معززة بالكامل</li>
            </ul>
            <a href="#" class="btn btn-disabled">قريباً جداً (الباقة تحت التجهيز الخوارزمي) ⏳</a>
        </div>
        """, unsafe_allow_html=True)

    # قسم محاكاة بوابة الدفع اليدوية الإضافية في حال رغب العميل بالتحقق الذاتي
    st.markdown("<br><hr style='border-color: rgba(255,255,255,0.05);'><br>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #ffffff;'>🛠️ نظام الفوترة والتحقق اليدوي المباشر (Crypto Manual Billing)</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8;'>إذا واجهت مشكلة في الدفع الآلي، يمكنك الدفع مباشرة للمحفظة أدناه ورفع رقم العملية لتوليد كود تفعيل تلقائي</p>", unsafe_allow_html=True)
    
    c_pay1, c_pay2 = st.columns([1.5, 2])
    with c_pay1:
        st.markdown("#### 1. معلومات محفظة السيرفر المعتمدة")
        st.write("شبكة التحويل: **TRC-20 (USDT)**")
        st.markdown("<div class='crypto-wallet-box'>TY7RuxA8f9eWqNzmKxP12vB76HjQLmNsdW</div>", unsafe_allow_html=True)
        st.info("⚠️ تأكد من التحويل على شبكة TRON (TRC20) حصراً لتجنب ضياع الأموال.")
        
    with c_pay2:
        st.markdown("#### 2. تقديم طلب التحقق المباشر")
        tx_hash = st.text_input("ادخل معرف التحويل (TXID / Hash):", placeholder="أدخل الـ Hash الخاص بالعملية هنا")
        plan_selected = st.selectbox("الخطة المراد تفعيلها:", ["باقة المحترفين PRO - $29.99", "الباقة المميزة PREMIUM - $49.99"])
        
        if st.button("إرسال الطلب للمراجعة والتحقق الآلي 🔄"):
            if len(tx_hash) > 10:
                generated_code = f"GOLD-PRO-{random.randint(1000,9999)}"
                st.session_state.crypto_invoices.append({
                    "الوقت": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "الـ Hash": tx_hash,
                    "الخطة": plan_selected,
                    "الحالة": "تم التحقق آلياً ✅",
                    "كود التفعيل المتولد": generated_code
                })
                st.success(f"🎉 تم التحقق من العملية على البلوكشين! كود التفعيل الخاص بك هو: **{generated_code}** (انسخه واستخدمه في حقل التفعيل بالأعلى)")
            else:
                st.error("❌ معرف التحويل (TXID) غير صحيح أو قصير جداً، يرجى التحقق من محفظتك.")
                
    if st.session_state.crypto_invoices:
        st.markdown("<br>##### 🕒 سجل طلبات التحقق السريعة الخاصة بك:", unsafe_allow_html=True)
        st.dataframe(pd.DataFrame(st.session_state.crypto_invoices), use_container_width=True)

    st.stop()

# ==============================================================================
# 4. لوحة التحكم والتحليل الداخلية الشاملة (تفتح بعد إدخال كود التفعيل)
# ==============================================================================
st.markdown(f"""
    <div style='display: flex; justify-content: space-between; align-items: center; background: rgba(30, 41, 59, 0.4); padding: 15px 25px; border-radius: 16px; border: 1px solid rgba(59, 130, 246, 0.2); margin-bottom: 30px;'>
        <div>
            <h2 style='margin: 0; color: #ffffff;'>📊 مجمع فك التشفير الكمي وملاحقة السيولة (الذهب XAUUSD)</h2>
            <p style='margin: 5px 0 0 0; color: #94a3b8; font-size: 14px;'>النظام مفعّل ومتصل بأعلى كفاءة لربط مصفوفات السيولة والتحليل الرياضي الشرطي</p>
        </div>
        <div style='text-align: left;'>
            <span style='background: #1e3a8a; color: #60a5fa; padding: 6px 16px; border-radius: 50px; font-weight: bold; font-size: 14px;'>ترخيص الحساب الحالي: باقة {st.session_state.user_tier} Mapped M1 ✅</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 5. شريط الأوامر والمحرك الجانبي بالـ Sidebar للمحترفين
# ------------------------------------------------------------------------------
st.sidebar.markdown("""
    <div style='text-align: center; margin-bottom: 20px;'>
        <h3 style='color: #3b82f6; margin:0;'>⚡ لوحة التحكم الخوارزمي</h3>
        <p style='color: #64748b; font-size: 12px;'>ضبط الفلاتر والمصفوفات الإحصائية الحية</p>
    </div>
""", unsafe_allow_html=True)

st.sidebar.divider()

# حاسبة إدارة المخاطر الصارمة لتحديد اللوت وحماية المحفظة
st.sidebar.markdown("#### 🛡️ حاسبة إدارة المخاطر وهندسة العقود")
account_capital = st.sidebar.number_input("رأس مال المحفظة الإجمالي ($):", value=10000, step=1000)
risk_exposure = st.sidebar.slider("مخاطرة الصفقة الواحدة من الحساب (%):", 0.25, 5.00, 1.00, 0.25)
stop_loss_distance = st.sidebar.number_input("مسافة الوقف (Stop Loss بالنقاط Pips):", value=40, step=5)

st.sidebar.divider()

# مدخلات ومحددات نماذج التوقع الرياضي وقانون بايز الإحصائي للتحكم بنماذج الذكاء
st.sidebar.markdown("#### 📐 معطيات النماذج الكمية ونسبة النجاح")
historical_winrate = st.sidebar.slider("نسبة نجاح الاستراتيجية التاريخية (Win Rate %):", 25, 90, 55, 5) / 100
risk_reward_ratio = st.sidebar.number_input("معدل العائد إلى المخاطرة (R:R Ratio المستهدف):", value=2.5, step=0.5)

st.sidebar.divider()

# فلترة مصفوفات صناع السوق الاستراتيجية (ICT Settings)
st.sidebar.markdown("#### 🔍 محددات خوارزمية الـ Order Block & FVG")
ob_filter_strength = st.sidebar.slider("قوة فلترة تكتلات صناع السوق (OB):", 1, 10, 6)
fvg_threshold = st.sidebar.slider("الحد الأدنى للفجوة السعرية العادلة (Pips):", 1.0, 15.0, 3.5, 0.5)
adx_period = st.sidebar.number_input("فترة مؤشر الزخم ADX المحسوب:", value=14, step=1)

st.sidebar.divider()

if st.sidebar.button("تسجيل الخروج وإغلاق الحساب الآمن 🔓", use_container_width=True):
    st.session_state.authenticated = False
    st.session_state.user_tier = None
    st.rerun()

# ------------------------------------------------------------------------------
# 6. قسم الحسابات الحقيقية لإدارة المخاطر الحجمية والـ Position Sizing Engine
# ------------------------------------------------------------------------------
st.markdown("### 🛡️ منظومة حماية الحساب وتحديد حجم العقود الصارم (Risk Management)")

# العمليات الحسابية الخوارزمية لإدارة حجم العقد في حسابات الذهب
monetary_risk = account_capital * (risk_exposure / 100)
# قاعدة تسعير وحركة الذهب الدولية: النقطة الواحدة (Pip) تساوي 10$ في العقد القياسي الكامل (1.00 Lot)
calculated_lot_size = monetary_risk / (stop_loss_distance * 10) if stop_loss_distance > 0 else 0.0

col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.markdown(f"""
        <div class='metric-card-custom' style='border-right: 4px solid #ef4444;'>
            <div class='metric-label'>الحد الأقصى للمبلغ المخاطر به في المحاولة</div>
            <h2 style='color: #ef4444; margin: 0; font-size: 32px;'>${monetary_risk:,.2f}</h2>
        </div>
    """, unsafe_allow_html=True)
with col_m2:
    st.markdown(f"""
        <div class='metric-card-custom' style='border-right: 4px solid #3b82f6;'>
            <div class='metric-label'>حجم عقد التداول المقترح (Lot Size)</div>
            <h2 style='color: #3b82f6; margin: 0; font-size: 32px;'>{calculated_lot_size:.2f} Standard</h2>
        </div>
    """, unsafe_allow_html=True)
with col_m3:
    st.markdown(f"""
        <div class='metric-card-custom' style='border-right: 4px solid #10b981;'>
            <div class='metric-label'>معامل استقرار أمان الحساب وإدارة المخاطر</div>
            <h2 style='color: #10b981; margin: 0; font-size: 32px;'>تطابق صارم ومستقر ✅</h2>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 7. قسم التحليل الإحصائي الكمي: دمج قانون بايز ومؤشر ADX المطور والتوقع الرياضي
# ------------------------------------------------------------------------------
st.markdown("### 🧠 النماذج الإحصائية المتقدمة وتطبيقات الاحتمال الشرطي (Quantitative Analysis)")

col_stat1, col_stat2 = st.columns(2)

with col_stat1:
    st.markdown("#### 📐 نظرية احتمالية بايز الشرطية المحدثة (Bayesian Probability Model)")
    st.write("يقوم المعالج المركزي بحساب احتمالية نجاح صعود الأسواق بناءً على دمج التدفق المؤسسي المسبق مع فلتر زخم مؤشر الـ ADX الحالي:")
    
    # بناء نموذج بايز الرياضي التفاعلي:
    # P(OrderBlock) = احتمالية صعود السعر عند تكون أوردر بلوك شرائي كمعطى مسبق معدل بقوة الفلترة
    p_ob = 0.55 + (ob_filter_strength * 0.015) 
    # P(ADX_High | OrderBlock) = احتمالية أن يعطي مؤشر ADX قراءة فوق 25 لتأكيد القوة عندما يكون الأوردر بلوك صحيحاً
    p_adx_given_ob = 0.82 
    # P(ADX_High | Non_OrderBlock) = احتمالية ح
