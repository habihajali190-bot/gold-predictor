import streamlit as st
import datetime
import urllib.request
import json
import streamlit.components.v1 as components

# 1. إعدادات الصفحة والعرض الكامل الاحترافي
st.set_page_config(page_title="Quantum Forex & Gold Bayesian Predictor Pro", page_icon="📊", layout="wide")

# 2. تصميم مخصص (CSS) لجعل الواجهة تطابق منصات التداول العالمية
st.markdown("""
<style>
    .stApp {
        background-color: #0c0f16;
        color: #ffffff;
    }
    div[data-testid="stBlock"] {
        background-color: #131722;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #202435;
        margin-bottom: 20px;
    }
    h1, h2, h3, h4 {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 600;
    }
    .pricing-card {
        background-color: #1c2030;
        border: 1px solid #2962ff;
        border-radius: 12px;
        padding: 25px;
        text-align: center;
        margin: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .pricing-header {
        color: #00ffcc;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .pricing-price {
        font-size: 32px;
        font-weight: 1000;
        color: #ffffff;
        margin: 15px 0;
    }
    .pricing-features {
        text-align: right;
        color: #b2b5be;
        font-size: 14px;
        line-height: 1.8;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# قاموس لربط الأزواج برمز ياهو فاينانس ورمز تيردينج فيو لمنع أي تعارض
ASSET_DICT = {
    "الذهب (XAUUSD)": {"yahoo": "GC=F", "tv": "OANDA:XAUUSD", "pip_value": 10},
    "يورو / دولار (EURUSD)": {"yahoo": "EURUSD=X", "tv": "FX:EURUSD", "pip_value": 10},
    "باوند / دولار (GBPUSD)": {"yahoo": "GBPUSD=X", "tv": "FX:GBPUSD", "pip_value": 10},
    "دولار / ين (USDJPY)": {"yahoo": "JPY=X", "tv": "FX:USDJPY", "pip_value": 100},
    "أسترالي / دولار (AUDUSD)": {"yahoo": "AUDUSD=X", "tv": "FX:AUDUSD", "pip_value": 10},
    "دولار / كندي (USDCAD)": {"yahoo": "CAD=X", "tv": "FX:USDCAD", "pip_value": 10},
    "باوند / ين (GBPJPY)": {"yahoo": "GBPJPY=X", "tv": "FX:GBPJPY", "pip_value": 100}
}

# دالة ذكية ومحمية لجلب السعر المباشر للزوج المختار من البورصة العالمية
def get_live_price(ticker):
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1m&range=1d"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            price = data['chart']['result'][0]['meta']['regularMarketPrice']
            return float(price)
    except Exception:
        # أسعار احتياطية قياسية في حال انقطاع السيرفر المؤقت لضمان استقرار السستم
        fallback_prices = {"GC=F": 2350.0, "EURUSD=X": 1.0850, "GBPUSD=X": 1.2600, "JPY=X": 155.0}
        return fallback_prices.get(ticker, 1.0)

# 3. إدارة حالة الجلسة لمنع الأخطاء البرمجية
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'chosen_plan' not in st.session_state:
    st.session_state['chosen_plan'] = None

# ==========================================
# واجهة خطط الاشتراك على طريقة TradingView
# ==========================================
if not st.session_state['authenticated']:
    st.markdown("<h1 style='text-align: center; color: #ffffff;'>📈 اختر خطة الاشتراك لبدء التداول</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #787b86; font-size: 16px;'>انضم إلى المتداولين المحترفين واستخدم الخوارزمية الإحصائية المتقدمة للذهب والفوركس</p>", unsafe_allow_html=True)
    st.write("<br>", unsafe_allow_html=True)
    
    plan_col1, plan_col2, plan_col3 = st.columns(3)
    
    with plan_col1:
        st.markdown("""
        <div class="pricing-card" style="border-color: #434651;">
            <div class="pricing-header" style="color: #787b86;">الخطة المجانية (Basic)</div>
            <div class="pricing-price">$0 <span style="font-size:14px; color:#787b86;">/ شهرياً</span></div>
            <div class="pricing-features">
                ⚫ شارت عادي فقط لسوق واحد<br>
                ⚫ تحديث متأخر للأسعار والبيانات<br>
                ❌ بدون الإشارات الإحصائية لبايز<br>
                ❌ بدون حاسبة إدارة المخاطر واللوت
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("بدء النسخة المحدودة مجاناً", key="btn_free"):
            st.error("عذراً، التسجيل في الخطة المجانية مغلق حالياً بسبب ضغط السيرفر. يرجى اختيار خطة مدفوعة.")
            
    with plan_col2:
        st.markdown("""
        <div class="pricing-card" style="border-color: #2962ff; background-color: #171b26;">
            <div class="pricing-header" style="color: #2962ff;">خطة برو المحترفة (Pro) ⭐</div>
            <div class="pricing-price">$29.99 <span style="font-size:14px; color:#787b86;">/ شهرياً</span></div>
            <div class="pricing-features">
                ✅ شارت TradingView الحي والتفاعلي بالكامل<br>
                ✅ سوق الفوركس كاملاً + سوق الذهب العالمي<br>
                ✅ تحديث حي وتلقائي للأسعار من البورصة<br>
                ✅ حاسبة لوت ذكية متوافقة مع حسابك
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("اشترك الآن في خطة PRO 🚀", key="btn_pro"):
            st.session_state['authenticated'] = True
            st.session_state['chosen_plan'] = "Pro Forex & Gold Trader"
            st.rerun()
            
    with plan_col3:
        st.markdown("""
        <div class="pricing-card" style="border-color: #ff9800;">
            <div class="pricing-header" style="color: #ff9800;">الخطة الحوت (Premium)</div>
            <div class="pricing-price">$59.99 <span style="font-size:14px; color:#787b86;">/ شهرياً</span></div>
            <div class="pricing-features">
                ✅ كل مميزات خطة برو المتقدمة للفوركس<br>
                ✅ أولوية قصوى في معالجة البيانات بالسيرفر<br>
                ✅ دعم فني خاص لربط الاستراتيجيات بالـ API<br>
                ✅ مؤشرات حصرية مضافة للخوارزمية الكمية
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("اشترك الآن في خطة PREMIUM ✨", key="btn_prem"):
            st.session_state['authenticated'] = True
            st.session_state['chosen_plan'] = "Premium Multi-Asset Whale"
            st.rerun()
            
    st.stop()

# ==========================================
# واجهة المنصة الاحترافية بعد اختيار الخطة
# ==========================================

st.markdown(f"""
<div style='background-color: #131722; padding: 15px; border-radius: 12px; border: 1px solid #202435; margin-bottom: 25px;'>
    <div style='float: left; background-color: #2962ff; padding: 5px 15px; border-radius: 20px; font-size: 12px;'>حساب مفعّل: {st.session_state['chosen_plan']}</div>
    <h2 style='color: #00ffcc; margin: 0;'>📊 Quantum Forex & Gold Bayesian Predictor Pro</h2>
    <p style='color: #787b86; margin: 5px 0 0 0;'>منصة التحليل الإحصائي وإدارة المخاطر الحية لأسواق العملات الأجنبية والمعادن</p>
</div>
""", unsafe_allow_html=True)

if st.button("تسجيل الخروج أو تغيير الخطة 🚪"):
    st.session_state['authenticated'] = False
    st.session_state['chosen_plan'] = None
    st.rerun()

# تقسيم مساحة الموقع
col_input, col_chart = st.columns([3, 7])

with col_input:
    st.markdown("<h4 style='color: #00ffcc; border-bottom: 1px solid #202435; padding-bottom: 10px;'>📥 اختيار الأصل والمعطيات الإحصائية</h4>", unsafe_allow_html=True)
    
    # قائمة اختيار الأصل المالي (ذهب أو أزواج فوركس)
    selected_asset = st.selectbox("اختر زوج التداول المطلوب تحليله:", list(ASSET_DICT.keys()))
    
    # جلب معلومات الزوج المحدد وسعره الحي فوراً
    asset_info = ASSET_DICT[selected_asset]
    live_price = get_live_price(asset_info["yahoo"])
    
    # عرض السعر المباشر للزوج المختار
    current_price = st.number_input(f"السعر المباشر الحالي لـ {selected_asset}:", value=live_price, format="%.5f" if "USD" in asset_info["yahoo"] and asset_info["yahoo"] != "GC=F" else "%.2f")
    
    if st.button("تحديث السعر الحي الآن 🔄"):
        st.rerun()
        
    p_h = st.slider("% P(H) نسبة نجاح استراتيجيتك العامة:", min_value=1.0, max_value=99.0, value=60.0) / 100.0
    
    st.markdown("<h4 style='color: #2962ff; margin-top: 20px;'>🛸 فلاتر السلوك السعري (ICT Setup)</h4>", unsafe_allow_html=True)
    fvg = st.checkbox("(FVG) فجوة سعرية غير مغلقة")
    ob = st.checkbox("(Order Block) بلوك مؤسساتي مفعّل")
    bos = st.checkbox("(BOS / CHoCH) كسر الهيكل السعري")
    liquidity = st.checkbox("(Liquidity) سحب سيولة قريبة")
    
    trade_direction = st.radio("الاتجاه المتوقع للصفقة:", ["شراء (Buy)", "بيع (Sell)"])

    # حساب الاحتمالات الشرطية الرياضية بدقة
    weight = 1.0
    if fvg: weight *= 1.3
    if ob: weight *= 1.4
    if bos: weight *= 1.5
    if liquidity: weight *= 1.4
    
    posterior_p = (p_h * weight) / ((p_h * weight) + (1 - p_h)) if ((p_h * weight) + (1 - p_h)) != 0 else 0.5
    if posterior_p > 0.99: posterior_p = 0.99
    
    st.markdown("<h4 style='color: #ff9800; margin-top: 20px;'>🧮 إدارة مخاطر رأس المال</h4>", unsafe_allow_html=True)
    balance = st.number_input("إجمالي حجم المحفظة ($):", value=10000.0, step=100.0)
    risk_percent = st.slider("نسبة المخاطرة المرغوبة (%):", min_value=0.1, max_value=5.0, value=1.0) / 100.0
    sl_pips = st.number_input("نقاط وقف الخسارة (SL Pips):", value=40, step=5)
    
    risk_amount = balance * risk_percent
    
    # حساب حجم اللوت الدقيق بناءً على طبيعة نقاط الزوج المختار (فوركس أو ذهب) لضمان عدم حدوث خطأ حسابي
    lot_size = risk_amount / (sl_pips * asset_info["pip_value"]) if sl_pips > 0 else 0.01

with col_chart:
    st.markdown("<h4 style='color: #00ffcc; border-bottom: 1px solid #202435; padding-bottom: 10px;'>🚨 تقييم الخوارزمية الفوري لـ {0}</h4>".format(selected_asset), unsafe_allow_html=True)
    final_percentage = posterior_p * 100
    
    res_col1, res_col2 = st.columns(2)
    
    with res_col1:
        if final_percentage >= 75.0:
            st.markdown(f"""
            <div style='background-color: #2e7d32; padding: 15px; border-radius: 8px; text-align: center; color: white;'>
                <h4 style='margin: 0;'>🟢 إشارة دخول قوية: {trade_direction}</h4>
                <p style='margin: 5px 0 0 0; font-size: 15px;'>الاحتمال الشرطي للنجاح: <b>{final_percentage:.1f}%</b></p>
            </div>
            """, unsafe_allow_html=True)
        elif 55.0 <= final_percentage < 75.0:
            st.markdown(f"""
            <div style='background-color: #f57c00; padding: 15px; border-radius: 8px; text-align: center; color: white;'>
                <h4 style='margin: 0;'>🟡 وضعية انتظار: شروط ضعيفة</h4>
                <p style='margin: 5px 0 0 0; font-size: 15px;'>الاحتمال الشرطي للنجاح: <b>{final_percentage:.1f}%</b></p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style='background-color: #c62828; padding: 15px; border-radius: 8px; text-align: center; color: white;'>
                <h4 style='margin: 0;'>🔴 خطر عالي: تجنب الدخول</h4>
                <p style='margin: 5px 0 0 0; font-size: 15px;'>الاحتمال الشرطي للنجاح: <b>{final_percentage:.1f}%</b></p>
            </div>
            """, unsafe_allow_html=True)
            
    with res_col2:
        st.markdown(f"""
        <div style='background-color: #1c2030; padding: 12px; border-radius: 8px; border: 1px solid #2a2e3d; color: white; height: 100%; text-align: center;'>
            <p style='margin: 0; font-size: 13px; color: #787b86;'>قيمة المخاطرة المادية: <b style='color: #ef5350;'>${risk_amount:.2f}</b></p>
            <p style='margin: 4px 0 0 0; font-size: 16px; color: #00ffcc;'>حجم اللوت المقترح: <b>{lot_size:.4f} Lot</b></p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"<h4 style='color: #00ffcc; margin-top: 25px;'>📉 شارت TradingView التفاعلي الحي لزوج: {selected_asset}</h4>", unsafe_allow_html=True)
    
    # كود الشارت التفاعلي الذي يتغير ديناميكياً بناءً على اختيارك من القائمة
    tradingview_html = f"""
    <div class="tradingview-widget-container" style="height:700px; width:100%;">
      <div id="tradingview_chart" style="height:700px;"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({{
        "autosize": true,
        "symbol": "{asset_info['tv']}",
        "interval": "15",
        "timezone": "Etc/UTC",
        "theme": "dark",
        "style": "1",
        "locale": "ar",
        "enable_publishing": false,
        "hide_side_toolbar": false,
        "allow_symbol_change": true,
        "container_id": "tradingview_chart"
      }});
      </script>
    </div>
    """
    components.html(tradingview_html, height=710)
