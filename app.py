import streamlit as st
import datetime
import urllib.request
import json
import streamlit.components.v1 as components

# 1. إعدادات الصفحة والعرض الكامل الاحترافي
st.set_page_config(page_title="Quantum Forex & Gold Bayesian Predictor Pro", page_icon="📊", layout="wide")

# 2. تصميم مخصص (CSS) متطور لإصلاح الأزرار والواجهة الداكنة
st.markdown("""
<style>
    .stApp { background-color: #0c0f16; color: #ffffff; }
    div[data-testid="stBlock"] {
        background-color: #131722; padding: 20px; border-radius: 12px;
        border: 1px solid #202435; margin-bottom: 20px;
    }
    h1, h2, h3, h4 { font-family: 'Segoe UI', sans-serif; font-weight: 600; }
    .pricing-card {
        background-color: #1c2030; border: 1px solid #2962ff; border-radius: 12px;
        padding: 25px; text-align: center; margin: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .pricing-header { color: #00ffcc; font-size: 24px; font-weight: bold; margin-bottom: 10px; }
    .pricing-price { font-size: 32px; font-weight: 1000; color: #ffffff; margin: 15px 0; }
    .pricing-features { text-align: right; color: #b2b5be; font-size: 14px; line-height: 1.8; margin-bottom: 20px; }
    .crypto-box {
        background-color: #0c0f16; border: 1px dashed #ff9800; padding: 10px;
        border-radius: 6px; font-family: monospace; color: #ff9800; font-size: 13px; word-break: break-all; margin-bottom: 15px;
    }
    div.stButton > button {
        background-color: #2962ff !important; color: white !important; font-weight: bold !important;
        border-radius: 8px !important; border: none !important; padding: 10px 20px !important; width: 100% !important;
    }
    div.stButton > button:hover { background-color: #1e4bd8 !important; }
</style>
""", unsafe_allow_html=True)

MY_USDT_WALLET = "TNXrnHhVR43VXN9ivp5TWiQ7b1ygbt9jiP"

# قاموس الأصول المطور بدقة مع تحديد خصائص العقد لكل سوق
ASSET_DICT = {
    "البيتكوين (BTCUSD)": {"yahoo": "BTC-USD", "tv": "BINANCE:BTCUSDT", "type": "crypto"},
    "الذهب (XAUUSD)": {"yahoo": "GC=F", "tv": "OANDA:XAUUSD", "type": "commodity"},
    "يورو / دولار (EURUSD)": {"yahoo": "EURUSD=X", "tv": "FX:EURUSD", "type": "forex"},
    "باوند / دولار (GBPUSD)": {"yahoo": "GBPUSD=X", "tv": "FX:GBPUSD", "type": "forex"},
    "دولار / ين (USDJPY)": {"yahoo": "JPY=X", "tv": "FX:USDJPY", "type": "forex"}
}

def get_live_price(ticker):
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1m&range=1d"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            price = data['chart']['result'][0]['meta']['regularMarketPrice']
            return float(price)
    except Exception:
        try:
            if ticker == "BTC-USD":
                res = urllib.request.urlopen("https://api.coinbase.com/v2/prices/BTC-USD/spot", timeout=3)
                return float(json.loads(res.read().decode())['data']['amount'])
        except: pass
        fallback = {"BTC-USD": 67250.0, "GC=F": 2345.50, "EURUSD=X": 1.0845, "GBPUSD=X": 1.2610, "JPY=X": 156.20}
        return fallback.get(ticker, 1.0)

if 'authenticated' not in st.session_state: st.session_state['authenticated'] = False
if 'chosen_plan' not in st.session_state: st.session_state['chosen_plan'] = None

# واجهة خطط الاشتراك والنظام التجاري الآمن
if not st.session_state['authenticated']:
    st.markdown("<h1 style='text-align: center; color: #ffffff;'>📈 تفعيل الحساب المتقدم</h1>", unsafe_allow_html=True)
    st.write("<br>", unsafe_allow_html=True)
    plan_col1, plan_col2, plan_col3 = st.columns(3)
    
    with plan_col1:
        st.markdown('<div class="pricing-card" style="border-color: #434651;"><div class="pricing-header" style="color: #787b86;">خطة Basic</div><div class="pricing-price">$0</div><div class="pricing-features">⚫ شارت عادي فقط لسوق واحد<br>❌ بدون حسابات الاحتمال الإحصائي الكمي وبايز</div></div>', unsafe_allow_html=True)
        if st.button("بدء النسخة المحدودة", key="btn_free"): st.error("التسجيل في الخطة المجانية مغلق حالياً.")
            
    with plan_col2:
        st.markdown(f'<div class="pricing-card" style="border-color: #2962ff; background-color: #171b26;"><div class="pricing-header" style="color: #2962ff;">خطة Pro المحترفة ⭐</div><div class="pricing-price">$29.99</div><div class="pricing-features">✅ دمج معادلة بايز والتوقع الرياضي كمياً<br>✅ قراءة حية لمؤشر ADX الرياضي وقوة الاتجاه</div><div class="crypto-box">{MY_USDT_WALLET}</div></div>', unsafe_allow_html=True)
        tx_pro = st.text_input("أدخل معرف التحويل (TxID) لـ PRO:", placeholder="أدخل اسمك أو كود التفعيل الخاص بك...", key="input_pro")
        if st.button("طلب تفعيل خطة PRO 🚀", key="btn_pro"):
            if tx_pro == "حبيبي_تداول_99":
                st.session_state['authenticated'] = True
                st.session_state['chosen_plan'] = "Pro Quantitative Bayesian Account"
                st.rerun()
            elif tx_pro.strip() != "": st.info("📥 جاري مراجعة التحويل يدوياً من قبل الإدارة...")
            else: st.warning("⚠️ يرجى إدخال كود التفعيل!")
            
    with plan_col3:
        st.markdown(f'<div class="pricing-card" style="border-color: #ff9800;"><div class="pricing-header" style="color: #ff9800;">خطة Premium</div><div class="pricing-price">$59.99</div><div class="pricing-features">✅ جميع الميزات الكمية + ربط ذكي بالـ API الخاص بالتداول المباشر</div><div class="crypto-box">{MY_USDT_WALLET}</div></div>', unsafe_allow_html=True)
        tx_prem = st.text_input("أدخل معرف التحويل (TxID) لـ PREMIUM:", key="input_prem")
        if st.button("طلب تفعيل خطة PREMIUM ✨", key="btn_prem"):
            if tx_prem == "حبيبي_تداول_99":
                st.session_state['authenticated'] = True
                st.session_state['chosen_plan'] = "Premium Quantitative Bayesian Account"
                st.rerun()
            elif tx_prem.strip() != "": st.info("📥 جاري مراجعة التحويل يدويًا...")
    st.stop()

# ==========================================
# واجهة المنصة الإحصائية بعد الدخول بنجاح
# ==========================================
st.markdown(f"<div style='background-color: #131722; padding: 15px; border-radius: 12px; border: 1px solid #202435; margin-bottom: 25px;'><div style='float: left; background-color: #2962ff; padding: 5px 15px; border-radius: 20px; font-size: 12px;'>حساب مفعّل: {st.session_state['chosen_plan']}</div><h2 style='color: #00ffcc; margin: 0;'>📊 Quantum Forex & Gold Bayesian Predictor Pro</h2></div>", unsafe_allow_html=True)

col_input, col_chart = st.columns([3, 7])

with col_input:
    st.markdown("<h4 style='color: #00ffcc;'>📥 المدخلات الكمية والإحصائية</h4>", unsafe_allow_html=True)
    selected_asset = st.selectbox("اختر زوج التداول المطلوب تحليله:", list(ASSET_DICT.keys()))
    
    asset_info = ASSET_DICT[selected_asset]
    live_price = get_live_price(asset_info["yahoo"])
    
    price_format = "%.2f" if asset_info["type"] in ["crypto", "commodity"] else "%.5f"
    current_price = st.number_input(f"السعر الحالي لـ {selected_asset}:", value=live_price, format=price_format)
    
    if st.button("تحديث السعر الحي الآن 🔄"):
        st.rerun()
        
    p_h = st.slider("% P(H) الاحتمال المسبق (قوة استراتيجيتك التاريخية):", min_value=10.0, max_value=90.0, value=50.0) / 100.0
    
    st.markdown("<h4 style='color: #ff9800; margin-top: 15px;'>📈 مؤشر القوة الاتجاهية (ADX)</h4>", unsafe_allow_html=True)
    adx_value = st.slider("قيمة مؤشر ADX الحالي في السوق:", min_value=0, max_value=100, value=28)
    
    st.markdown("<h4 style='color: #2962ff; margin-top: 15px;'>🛸 فلاتر السلوك السعري (ICT Setups)</h4>", unsafe_allow_html=True)
    fvg = st.checkbox("(FVG) فجوة سعرية غير مغلقة")
    ob = st.checkbox("(Order Block) بلوك مؤسساتي مفعّل")
    bos = st.checkbox("(BOS / CHoCH) كسر الهيكل السعري")
    liquidity = st.checkbox("(Liquidity) سحب سيولة قريبة")
    
    trade_direction = st.radio("الاتجاه المتوقع للصفقة:", ["شراء (Buy)", "بيع (Sell)"])

    # الحساب الكمي القائم على قانون بايز
    likelihood_ratio = 1.0
    if adx_value > 25: likelihood_ratio *= 1.35
    elif adx_value < 20: likelihood_ratio *= 0.60
    if fvg: likelihood_ratio *= 1.25
    if ob: likelihood_ratio *= 1.35
    if bos: likelihood_ratio *= 1.40
    if liquidity: likelihood_ratio *= 1.30
    
    posterior_p = (p_h * likelihood_ratio) / ((p_h * likelihood_ratio) + (1 - p_h))
    posterior_p = max(0.01, min(0.99, posterior_p))
    
    st.markdown("<h4 style='color: #00ffcc; margin-top: 15px;'>🧮 إدارة مخاطر رأس المال المتقدمة</h4>", unsafe_allow_html=True)
    balance = st.number_input("إجمالي حجم المحفظة ($):", value=10000.0, step=100.0)
    risk_percent = st.slider("نسبة المخاطرة للمحفظة (%):", min_value=0.1, max_value=5.0, value=1.0) / 100.0
    
    # تفريع واجهة وقف الخسارة حسب نوع الأصل لمنع اللبس
    if asset_info["type"] == "crypto":
        sl_input = st.number_input("وقف الخسارة بالدولار (SL USD) - فارق السعر حركياً:", value=500.0, step=50.0)
        tp_input = st.number_input("أخذ الهدف بالدولار (TP USD) - فارق السعر حركياً:", value=1500.0, step=50.0)
        risk_to_reward = tp_input / sl_input if sl_input > 0 else 1
    else:
        sl_input = st.number_input("نقاط وقف الخسارة (SL Pips):", value=40, min_value=1)
        tp_input = st.number_input("نقاط أخذ الهدف (TP Pips):", value=120, min_value=1)
        risk_to_reward = tp_input / sl_input if sl_input > 0 else 1
    
    # حساب التوقع الرياضي
    p_success = posterior_p
    p_fail = 1.0 - p_success
    mathematical_expectation = (p_success * risk_to_reward) - p_fail
    
    # 🌟 الحساب البرمجي الدقيق والمصلح لحجم اللوت (Lot Size) حسب معايير الأسواق العالمية
    risk_amount = balance * risk_percent
    
    if asset_info["type"] == "crypto":
        # للبيتكوين: المخاطرة المادية تقسيم فارق السعر بالدولار مباشرة
        calculated_lot = risk_amount / sl_input if sl_input > 0 else 0.01
        lot_label = "حجم عقد البيتكوين (BTC)"
    elif asset_info["type"] == "commodity":
        # للذهب: النقطة الواحدة في اللوت القياسي (100 أونصة) تساوي 10$ عند تحرك الذهب 10 سنتات. 
        # بالتالي: حجم اللوت = المخاطرة / (عدد النقاط * 0.10 * 10)
        calculated_lot = risk_amount / (sl_input * 1.0) if sl_input > 0 else 0.01
        lot_label = "حجم لوت الذهب (Standard Lot)"
    else:
        # للفوركس: النقطة في اللوت القياسي للأزواج الرئيسية تساوي 10$
        if "JPY" in asset_info["yahoo"]:
            calculated_lot = risk_amount / (sl_input * 6.5) if sl_input > 0 else 0.01 # تعديل للياباني
        else:
            calculated_lot = risk_amount / (sl_input * 10.0) if sl_input > 0 else 0.01
        lot_label = "حجم لوت الفوركس (Standard Lot)"

with col_chart:
    st.markdown(f"<h4 style='color: #00ffcc;'>🚨 تقييم الخوارزمية الكمية لـ {selected_asset}</h4>", unsafe_allow_html=True)
    final_percentage = posterior_p * 100
    
    res_col1, res_col2, res_col3 = st.columns(3)
    
    with res_col1:
        st.markdown(f"""
        <div style='background-color: #171b26; padding: 15px; border-radius: 8px; text-align: center; border: 1px solid #202435;'>
            <p style='margin:0; font-size:12px; color:#787b86;'>احتمالية بايز اللاحقة P(H|E)</p>
            <h3 style='margin:5px 0; color:#00ffcc;'>{final_percentage:.1f}%</h3>
        </div>
        """, unsafe_allow_html=True)
        
    with res_col2:
        exp_color = "#2e7d32" if mathematical_expectation > 0 else "#c62828"
        st.markdown(f"""
        <div style='background-color: #171b26; padding: 15px; border-radius: 8px; text-align: center; border: 1px solid #202435;'>
            <p style='margin:0; font-size:12px; color:#787b86;'>التوقع الرياضي E[X]</p>
            <h3 style='margin:5px 0; color:{exp_color};'>{mathematical_expectation:.2f}</h3>
        </div>
        """, unsafe_allow_html=True)
        
    with res_col3:
        st.markdown(f"""
        <div style='background-color: #171b26; padding: 15px; border-radius: 8px; text-align: center; border: 1px solid #202435;'>
            <p style='margin:0; font-size:12px; color:#787b86;'>{lot_label}</p>
            <h3 style='margin:5px 0; color:#ff9800;'>{calculated_lot:.2f}</h3>
        </div>
        """, unsafe_allow_html=True)
        
    st.write("<br>", unsafe_allow_html=True)
    if mathematical_expectation > 0.2 and final_percentage >= 60.0:
        st.markdown(f"<div style='background-color:#2e7d32; padding:15px; border-radius:8px; text-align:center;'><b>🟢 إشارة دخول مفعّلة: {trade_direction} (توقع رياضي إيجابي مستدام واللوت محسوب بدقة تامة للمنصة)</b></div>", unsafe_allow_html=True)
    elif adx_value < 20:
        st.markdown("<div style='background-color:#f57c00; padding:15px; border-radius:8px; text-align:center;'><b>⚠️ تحذير كمي: مؤشر ADX يشير إلى سوق عرضي ميت! تجنب المخاطرة.</b></div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='background-color:#c62828; padding:15px; border-radius:8px; text-align:center;'><b>🔴 النظام يوصي بالابتعاد: التوقع الرياضي خاسر على المدى الطويل.</b></div>", unsafe_allow_html=True)

    st.markdown(f"<h4 style='color: #00ffcc; margin-top: 25px;'>📉 شارت TradingView التفاعلي الحي: {selected_asset}</h4>", unsafe_allow_html=True)
    tradingview_html = f"""
    <div class="tradingview-widget-container" style="height:600px; width:100%;">
      <div id="tradingview_chart" style="height:600px;"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({{
        "autosize": true, "symbol": "{asset_info['tv']}", "interval": "15",
        "timezone": "Etc/UTC", "theme": "dark", "style": "1", "locale": "ar",
        "enable_publishing": false, "container_id": "tradingview_chart"
      }});
      </script>
    </div>
    """
    components.html(tradingview_html, height=610)
