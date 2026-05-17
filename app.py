import streamlit as st
import datetime
import urllib.request
import json
import random
import streamlit.components.v1 as components

# إعدادات الصفحة
st.set_page_config(page_title="Quantum Institutional Bayesian Hub", page_icon="⚡", layout="wide")

# 1. قاعدة بيانات أكواد التفعيل (تستطيع توليدها وبيعها عبر متجر أوتوماتيكي مثل Sellix)
# كل كود مخصص لباقة معينة، وبمجرد دخوله يتم تفعيل المنصة بناءً عليه.
VALID_CODES = {
    "PRO-9942-X1": "Pro",
    "PRO-1120-M5": "Pro",
    "PRO-8839-L2": "Pro",
    "PREM-5561-Z9": "Premium",
    "PREM-7740-Q3": "Premium",
    "PREM-3312-W4": "Premium"
}

# الكود السري الخاص بك كمالك للمنصة (يفتح كل شيء دائماً)
ADMIN_CODE = "حبيبي_تداول_99"

# 2. تصميم الـ UI الاحترافي للموقع
st.markdown("""
<style>
    .stApp { background-color: #060811; color: #ffffff; }
    div[data-testid="stBlock"] {
        background-color: #0d111c; padding: 25px; border-radius: 16px;
        border: 1px solid #1e293b; margin-bottom: 20px;
    }
    .pricing-card {
        background: linear-gradient(180deg, #111827, #030712); border: 1px solid #3b82f6;
        border-radius: 16px; padding: 35px; text-align: center; margin: 10px;
    }
    .pricing-header { color: #38bdf8; font-size: 24px; font-weight: 800; }
    .pricing-price { font-size: 38px; font-weight: 900; color: #ffffff; margin: 15px 0; }
    .pricing-features { text-align: right; color: #9ca3af; font-size: 14px; line-height: 2; margin-bottom: 25px; }
    .crypto-box {
        background-color: #030712; border: 1px dashed #f59e0b; padding: 12px;
        border-radius: 8px; font-family: monospace; color: #f59e0b; font-size: 14px; word-break: break-all;
    }
    .buy-button {
        display: block; background: linear-gradient(90deg, #059669, #10b981); color: white !important;
        text-align: center; font-weight: bold; padding: 12px; border-radius: 8px;
        text-decoration: none; margin-top: 15px; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
    }
    div.stButton > button {
        background: linear-gradient(90deg, #1d4ed8, #2563eb) !important; color: white !important;
        font-weight: 700 !important; border-radius: 10px !important; border: none !important;
        padding: 12px 24px !important; width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)

MY_USDT_WALLET = "TNXrnHhVR43VXN9ivp5TWiQ7b1ygbt9jiP"

ASSET_DICT = {
    "البيتكوين (BTCUSD)": {"yahoo": "BTC-USD", "tv": "BINANCE:BTCUSDT", "type": "crypto"},
    "الذهب (XAUUSD)": {"yahoo": "GC=F", "tv": "OANDA:XAUUSD", "type": "commodity"},
    "يورو / دولار (EURUSD)": {"yahoo": "EURUSD=X", "tv": "FX:EURUSD", "type": "forex"}
}

if 'authenticated' not in st.session_state: st.session_state['authenticated'] = False
if 'user_plan' not in st.session_state: st.session_state['user_plan'] = None

# واجهة خطط الاشتراكات المؤتمتة
if not st.session_state['authenticated']:
    st.markdown("<h1 style='text-align: center; color: #ffffff; font-size: 36px;'>⚡ QUANTUM INSTITUTIONAL HUB</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 16px;'>منصة التحليل الإحصائي التطبيقي وإدارة المخاطر الكمية المصرفية</p>", unsafe_allow_html=True)
    st.write("<br>", unsafe_allow_html=True)
    
    plan_col1, plan_col2 = st.columns(2)
    with plan_col1:
        st.markdown(f"""
        <div class="pricing-card">
            <div class="pricing-header">💼 باقة المحترفين (PRO)</div>
            <div class="pricing-price">$29.99 <span style="font-size:14px; color:#64748b;">/ شهرياً</span></div>
            <div class="pricing-features">
                ✅ دمج قانون بايز الإحصائي والاحتمالات اللاحقة<br>
                ✅ حاسبة اللوت الديناميكية المصححة للأصول والذهب والـ BTC<br>
                ✅ شارت تفاعلي حي ومؤشر القوة الاتجاهية ADX العملياتي
            </div>
            <div class="crypto-box">{MY_USDT_WALLET}</div>
            <a class="buy-button" href="https://sellix.io" target="_blank">شراء كود التفعيل الفوري تيكت 💳</a>
        </div>
        """, unsafe_allow_html=True)
        
    with plan_col2:
        st.markdown(f"""
        <div class="pricing-card" style="border-color: #eab308;">
            <div class="pricing-header" style="color: #eab308;">👑 باقة الحيتان (PREMIUM)</div>
            <div class="pricing-price">$59.99 <span style="font-size:14px; color:#64748b;">/ شهرياً</span></div>
            <div class="pricing-features">
                ✅ جميع ميزات باقة PRO الكمية المتقدمة<br>
                ✅ معالجة التوقع الرياضي المركب لحماية حسابات التمويل<br>
                ✅ أولوية تحديث فوري لأسعار عقود الفروقات لايف دون كاش
            </div>
            <div class="crypto-box">{MY_USDT_WALLET}</div>
            <a class="buy-button" href="https://sellix.io" target="_blank" style="background: linear-gradient(90deg, #d97706, #f59e0b);">شراء كود التفعيل الفوري تيكت 💳</a>
        </div>
        """, unsafe_allow_html=True)
        
    _, input_col, _ = st.columns([1, 2, 1])
    with input_col:
        # هنا يقوم العميل بلصق الكود الذي اشتراه من المتجر الأوتوماتيكي
        entered_code = st.text_input("أدخل كود التفعيل الفوري (أو كود المالك السري):", type="password")
        if st.button("تفعيل المنصة وفك التشفير الكمي 🔓"):
            if entered_code == ADMIN_CODE:
                st.session_state['authenticated'] = True
                st.session_state['user_plan'] = "المالك الاستراتيجي للمنصة (بريميوم)"
                st.rerun()
            elif entered_code in VALID_CODES:
                st.session_state['authenticated'] = True
                st.session_state['user_plan'] = f"عضوية {VALID_CODES[entered_code]} النشطة"
                # ملاحظة: برمجياً في الأنظمة الكبيرة نقوم بحذف الكود من قاعدة البيانات هنا لكي لا يُستخدم مجدداً
                st.rerun()
            elif entered_code.strip() != "":
                st.error("❌ كود التفعيل غير صحيح، منتهي الصلاحية، أو لم يتم تأكيد التحويل بعد.")
            else:
                st.warning("⚠️ يرجى كتابة كود التفعيل.")
    st.stop()

# ==========================================
# واجهة التطبيق بعد الدفع والتفعيل بنجاح
# ==========================================
st.markdown(f"<div style='background-color: #111827; padding: 10px; border-radius: 8px; border: 1px solid #1f2937; margin-bottom: 20px;'><p style='margin:0; color:#10b981; font-weight:bold;'>🔓 تم تفعيل الحساب بنجاح: {st.session_state['user_plan']}</p></div>", unsafe_allow_html=True)
st.write("### مرحباً بك في المنصة الرياضية الحية...")
# (باقي الكود الإحصائي للـ ADX وبايز وحساب اللوت والـ TradingView يوضع هنا طبيعياً)
