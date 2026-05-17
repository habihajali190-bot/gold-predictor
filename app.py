import streamlit as st
import datetime
import streamlit.components.v1 as components

# إعدادات الصفحة الفخمة
st.set_page_config(page_title="Gold Bayesian Quantum Predictor", page_icon="📊", layout="wide")

# ==========================================
# قاعدة بيانات المشتركين وتواريخ انتهاء الصلاحية
# ==========================================
SUBSCRIBERS = {
    "STAT-TRADER-99": {"owner": "Habib (المطور)", "expiry": datetime.date(2030, 1, 1)},
    "GOLD-777-BAYES": {"owner": "عميل أول", "expiry": datetime.date(2026, 6, 15)},
    "ICT-PRO-2026": {"owner": "عميل ثانٍ", "expiry": datetime.date(2026, 5, 30)}
}

# التحقق من حالة الجلسة
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'user_key' not in st.session_state:
    st.session_state['user_key'] = ""

# واجهة قفل النظام والاشتراكات
if not st.session_state['authenticated']:
    st.markdown("<h1 style='text-align: center; color: #f1c40f;'>🔐 Gold Bayesian Predictor (النسخة المدفوعة)</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #bdc3c7;'>هذا النظام الإحصائي محمي ومخصص للمشتركين فقط لتحليل أسواق المال والذهب</p>", unsafe_allow_html=True)
    st.write("---")
    
    token_input = st.text_input("🔑 أدخل مفتاح التفعيل الخاص بك لتشغيل النظام:", type="password")
    
    if st.button("تفعيل التطبيق واستخدام النظام"):
        if token_input in SUBSCRIBERS:
            today = datetime.date.today()
            expiry_date = SUBSCRIBERS[token_input]["expiry"]
            
            if today <= expiry_date:
                st.session_state['authenticated'] = True
                st.session_state['user_key'] = token_input
                st.success(f"🔓 تم التفعيل بنجاح! أهلاً بك.")
                st.rerun()
            else:
                st.error(f"❌ هذا المفتاح انتهت صلاحيته بتاريخ ({expiry_date}).")
        else:
            st.error("❌ مفتاح التفعيل غير صحيح!")
    st.stop()

# واجهة المنصة بعد التفعيل
user_info = SUBSCRIBERS[st.session_state['user_key']]
st.markdown(f"<h1 style='text-align: center; color: #00ffcc;'>📊 Gold Bayesian Quantum Predictor | Premium Version</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #95a5a6;'>مرحباً بك: <b>{user_info['owner']}</b> | صلاحية الاشتراك مفعّلة لغاية: <b>{user_info['expiry']}</b></p>", unsafe_allow_html=True)

if st.button("تسجيل الخروج 🚪"):
    st.session_state['authenticated'] = False
    st.session_state['user_key'] = ""
    st.rerun()

st.write("---")
col_left, col_right = st.columns([4, 6])

with col_left:
    st.markdown("### 📥 مدخلات البيانات الإحصائية")
    current_price = st.number_input("(XAUUSD) سعر الذهب أو الزوج الحالي:", value=2350.00, step=1.0)
    p_h = st.slider("% P(H) نسبة النجاح العامة لاستراتيجيتك الحالية:", min_value=1.0, max_value=99.0, value=60.0) / 100.0
    
    st.markdown("#### 🛸 شروط خوارزمية السعر (ICT Setup)")
    fvg = st.checkbox("(Fair Value Gap / FVG) وجود فجوة سعرية")
    ob = st.checkbox("(Order Block / OB) وجود بلوك صانع سوق")
    bos = st.checkbox("(BOS / CHoCH) كسر هيكل السوق أو تغير الاتجاه")
    liquidity = st.checkbox("(Liquidity Sweep) سحب سيولة مكشوفة")
    
    trade_direction = st.radio("اختر نوع الصفقة المخطط لها:", ["شراء (Buy)", "بيع (Sell)"])

    # خوارزمية بايز لحساب الاحتمالات الشرطية للفوركس
    weight = 1.0
    if fvg: weight *= 1.3
    if ob: weight *= 1.4
    if bos: weight *= 1.5
    if liquidity: weight *= 1.4
    
    posterior_p = (p_h * weight) / ((p_h * weight) + (1 - p_h))
    if posterior_p > 0.99: posterior_p = 0.99
    
    st.markdown("#### 🧮 حجم العقود وإدارة الحساب (Risk Management)")
    balance = st.number_input("حجم الحساب الإجمالي ($):", value=10000.0, step=100.0)
    risk_percent = st.slider("نسبة المخاطرة للمحفظة (%):", min_value=0.1, max_value=5.0, value=1.0) / 100.0
    sl_pips = st.number_input("عدد نقاط وقف الخسارة (SL Pips):", value=40, step=5)
    
    risk_amount = balance * risk_percent
    lot_size = risk_amount / (sl_pips * 10) if sl_pips > 0 else 0.01

with col_right:
    st.markdown("### 🚨 إشارة الدخول والتحليل الفوري")
    final_percentage = posterior_p * 100
    
    if final_percentage >= 75.0:
        st.markdown(f"""
        <div style='background-color: #2ecc71; padding: 20px; border-radius: 10px; text-align: center; color: white;'>
            <h2 style='margin: 0;'>🟢 إشارة دخول صريحة: {trade_direction}</h2>
            <p style='margin: 5px 0 0 0; font-size: 18px;'>الاحتمال الإحصائي للنجاح قوي جداً ويساوي: <b>{final_percentage:.1f}%</b></p>
        </div>
        """, unsafe_allow_html=True)
    elif 55.0 <= final_percentage < 75.0:
        st.markdown(f"""
        <div style='background-color: #f39c12; padding: 20px; border-radius: 10px; text-align: center; color: white;'>
            <h2 style='margin: 0;'>🟡 انتظر: الشروط غير كافية</h2>
            <p style='margin: 5px 0 0 0; font-size: 18px;'>الاحتمال الشرطي الحالي: <b>{final_percentage:.1f}%</b></p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style='background-color: #e74c3c; padding: 20px; border-radius: 10px; text-align: center; color: white;'>
            <h2 style='margin: 0;'>🔴 مخاطرة عالية: تجنب الدخول</h2>
            <p style='margin: 5px 0 0 0; font-size: 18px;'>احتمال نجاح الصفقة هابط ويساوي: <b>{final_percentage:.1f}%</b></p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("#### 📊 خطة العقد وإدارة المخاطر المقترحة")
    st.info(f"""
    * **المبلغ المخاطر به في هذه الصفقة:** ${risk_amount:.2f}
    * **حجم اللوت (Lot Size) المناسب تماماً لحسابك:** {lot_size:.2f} لوت
    """)
    
    st.markdown("---")
    st.markdown("### 📉 الشارت الحي والتفاعلي الشامل (TradingView)")
    
    tradingview_html = """
    <div class="tradingview-widget-container" style="height:500px;width:100%;">
      <div id="tradingview_chart"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({
        "autosize": true,
        "symbol": "OANDA:XAUUSD",
        "interval": "15",
        "timezone": "Etc/UTC",
        "theme": "dark",
        "style": "1",
        "locale": "ar",
        "enable_publishing": false,
        "hide_side_toolbar": false,
        "allow_symbol_change": true,
        "container_id": "tradingview_chart"
      });
      </script>
    </div>
    """
    components.html(tradingview_html, height=520)
