import streamlit as st
import pandas as pd
import math

# إعدادات الصفحة الافتراضية
st.set_page_config(page_title="Gold Bayesian Quantum Predictor Pro", page_icon="🪙", layout="wide")

# قائمة المفاتيح الصالحة لإدارة المشتركين
VALID_KEYS = ["GOLD-777-BAYES", "ICT-PRO-2026", "STAT-TRADER-99"]

# ستايل داكن واحترافي
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; background-color: #ffaa00; color: black; font-weight: bold; }
    .go-signal { background-color: #04b431; padding: 20px; text-align: center; border-radius: 10px; font-size: 24px; font-weight: bold; }
    .nogo-signal { background-color: #df0101; padding: 20px; text-align: center; border-radius: 10px; font-size: 24px; font-weight: bold; }
    .lock-screen { text-align: center; padding: 50px; background-color: #1a1c23; border-radius: 15px; border: 2px solid #ffaa00; }
    </style>
""", unsafe_allow_html=True)

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# شاشة القفل وطلب الدفع للمشتركين
if not st.session_state['authenticated']:
    st.markdown("""
        <div class="lock-screen">
            <h1 style='color: #ffaa00;'>🪙 Gold Bayesian Predictor (النسخة المدفوعة Pro)</h1>
            <p>هذا النظام الإحصائي محمي ومخصص للمشتركين فقط لمنع التداول العشوائي على الذهب.</p>
            <p>للحصول على مفتاح التفعيل والاشتراك، يرجى التواصل مع الإدارة مباشرة.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    user_key = st.text_input("🔑 أدخل مفتاح التفعيل الخاص بك لتشغيل النظام:", type="password")
    
    if st.button("تفعيل التطبيق واستخدام النظام"):
        if user_key in VALID_KEYS:
            st.session_state['authenticated'] = True
            st.success("تم التفعيل بنجاح! جاري فتح النظام...")
            st.rerun()
        else:
            st.error("مفتاح التفعيل غير صحيح أو منتهي الصلاحية!")
else:
    if st.sidebar.button("🔒 قفل التطبيق والأمان"):
        st.session_state['authenticated'] = False
        st.rerun()

    st.title("🪙 نظام الاحتمالات الإحصائي لتداول الذهب (ICT + Bayes)")
    st.subheader("النسخة التجارية المدفوعة | Premium Version")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.header("📥 مدخلات البيانات")
        price = st.number_input("سعر الذهب الحالي (XAUUSD):", min_value=0.0, value=2350.0, step=0.1)
        base_win_rate = st.slider("نسبة النجاح العامة لاستراتيجيتك P(H) %:", 10, 90, 60) / 100.0
        
        st.write("---")
        st.write("**شروط خوارزمية السعر (ICT Setup):**")
        fvg = st.checkbox("وجود فجوة سعرية (Fair Value Gap / FVG)")
        ob = st.checkbox("وجود بلوك صانع سوق (Order Block / OB)")
        bos = st.checkbox("كسر هيكل السوق أو تغير الاتجاه (BOS / CHoCH)")
        liquidity = st.checkbox("سحب سيولة مكشوفة (Liquidity Sweep)")
        
        st.write("---")
        adx_value = st.number_input("قراءة مؤشر قوة الاتجاه (ADX):", min_value=0.0, max_value=100.0, value=25.0)
        
        st.write("---")
        st.write("**إدارة المخاطر لحسابات التمويل:**")
        balance = st.number_input("حجم الحساب الحالي ($):", min_value=0.0, value=10000.0)
        risk_pct = st.slider("نسبة المخاطرة للصفقة %:", 0.25, 5.0, 1.0) / 100.0
        sl_pips = st.number_input("وقف الخسارة بالنقاط (SL Pips):", min_value=5, value=30)
        rr_ratio = st.number_input("نسبة العائد إلى المخاطرة المستهدفة (Risk:Reward):", min_value=1.0, value=2.0, step=0.5)

    # حساب منطق بايز والاحتمالات الشرطية
    ict_score = sum([fvg, ob, bos, liquidity])

    if ict_score >= 3:
        p_a_h = 0.88
        p_a_noth = 0.30
    elif ict_score == 2:
        p_a_h = 0.75
        p_a_noth = 0.45
    elif ict_score == 1:
        p_a_h = 0.55
        p_a_noth = 0.60
    else:
        p_a_h = 0.30
        p_a_noth = 0.85

    if adx_value >= 25:
        p_a_h = min(p_a_h * 1.15, 0.99)
        p_a_noth = p_a_noth * 0.80
    else:
        p_a_h = p_a_h * 0.75
        p_a_noth = min(p_a_noth * 1.20, 0.99)

    p_noth = 1.0 - base_win_rate
    p_a = (p_a_h * base_win_rate) + (p_a_noth * p_noth)
    final_prob = (p_a_h * base_win_rate) / p_a if p_a > 0 else 0.0

    # حسابات إدارة المخاطر الصارمة
    risk_amount = balance * risk_pct
    lot_size = risk_amount / (sl_pips * 10)
    
    # حساب التوقع الرياضي الفعلي للصفقة E(X)
    expected_value = (final_prob * rr_ratio) - (1.0 - final_prob)
    
    # حساب سلسلة الخسائر المتتالية المحتملة إحصائياً لحماية التمويل
    if final_prob < 0.99:
        max_losses_streak = math.log(0.01) / math.log(1.0 - final_prob) if final_prob > 0 else 1
    else:
        max_losses_streak = 1

    with col2:
        st.header("📊 المخرجات والتحليل الإحصائي")
        
        if final_prob >= 0.75 and expected_value > 0:
            st.markdown(f'<div class="go-signal">إشارة الدخول: GO (تأكيد إحصائي وتوقع رياضي إيجابي) 🚀</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="nogo-signal">إشارة الدخول: NO GO (مخاطرة عالية أو عشوائية سعرية) ❌</div>', unsafe_allow_html=True)
            
        st.write("")
        metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
        metrics_col1.metric("الاحتمال الأولي P(H)", f"{base_win_rate*100:.1f}%")
        metrics_col2.metric("التوقع الرياضي E(X)", f"+{expected_value:.2f}" if expected_value > 0 else f"{expected_value:.2f}")
        metrics_col3.metric("الاحتمالية النهائية المعدلة", f"{final_prob*100:.1f}%")
        
        st.write("---")
        st.subheader("🧮 حجم العقود وإدارة الـ Drawdown")
        
        st.info(f"""
        * **المبلغ المخاطر به في هذه الصفقة:** ${risk_amount:.2f}
        * **حجم اللوت المناسب لعقد الذهب الحالي:** `{lot_size:.2f}` Lot
        * **الهدف المقترح (Take Profit) بالنقاط:** {sl_pips * rr_ratio:.0f} نقطة.
        """)
        
        st.write("---")
        st.subheader("💡 النصائح الاحترافية وحماية الحساب")
        if final_prob >= 0.75:
            st.success(f"""
            **تحليل الصفقة:** تطابق شروط الـ ICT مع زخم الـ ADX عند السعر {price} يعطيك أرجحية عالية جداً. 
            إحصائياً، أسوأ سلسلة خسائر متتالية متوقعة لهذه الاحتمالية هي {max_losses_streak:.0f} صفقات فقط، وبالتالي حساب التمويل الخاص بك في أمان كامل مع هذا اللوت.
            """)
        else:
            st.warning(f"""
            **تحذير إحصائي:** الاحتمالية النهائية منخفضة والتوقع الرياضي الحالي ({expected_value:.2f}) يضعك في خانة خسارة رأس المال على المدى الطويل.
            السوق الآن يقترب من توزيع 'المتحول العشوائي المنتظم' (حظ 50/50)، يفضل انتظار سحب سيولة واضح أو فجوة سعرية جديدة لكسر هذه العشوائية.
            """)