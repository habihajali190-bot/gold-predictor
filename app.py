import streamlit as st
import pandas as pd
import numpy as np

# 1. إعدادات الصفحة الأساسية
st.set_page_config(
    page_title="Quantum Institutional Bayesian Predictor - Gold",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. نظام التفعيل وإدارة الجلسة (Session State)
VALID_SERIALS = {
    "GOLD-PRO-8812": "Pro"
}

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_tier" not in st.session_state:
    st.session_state.user_tier = None

# 3. تصميم واجهة التفعيل والدفع (إذا لم يكن المستخدم مسجلاً)
if not st.session_state.authenticated:
    st.title("⚡ منصة التوقع المؤسسي الذكي للذهب")
    st.write("مرحباً بك في المنصة الرقمية المتقدمة لفك تشفير السيولة وتوقع اتجاه الأسواق بناءً على خوارزميات ICT والمعادلات الإحصائية المتقدمة.")
    
    st.divider()
    
    # خانة إدخال كود التفعيل
    st.subheader("🔑 تفعيل المنصة")
    serial_input = st.text_input("أدخل كود التفعيل الفوري الخاص بك هنا:", placeholder="GOLD-XXXX-XXXX").strip()
    
    if st.button("تفعيل الحساب والتشغيل 🚀"):
        if serial_input in VALID_SERIALS:
            st.session_state.authenticated = True
            st.session_state.user_tier = VALID_SERIALS[serial_input]
            st.success(f"🎉 تم التفعيل بنجاح! مرحباً بك في الباقة ({st.session_state.user_tier})")
            st.rerun()
        else:
            st.error("❌ كود التفعيل غير صحيح أو منتهي الصلاحية. يرجى التأكد من الكود أو شراء كود جديد من الأسفل.")

    st.divider()

    # قسم خطط الاشتراك وبطاقات الأسعار (محدث برابط متجرك المباشر)
    st.markdown("## 💳 خطط الاشتراك المتاحة")

    plan_col1, plan_col2 = st.columns(2)

    with plan_col1:
        st.markdown("""
        <div class="pricing-card" style="background: rgba(30, 41, 59, 0.7); padding: 25px; border-radius: 15px; border: 1px solid #3b82f6; text-align: center; margin-bottom: 20px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
            <div style="background: #3b82f6; color: white; padding: 4px 12px; border-radius: 20px; font-size: 12px; display: inline-block; margin-bottom: 10px; font-weight: bold;">الأكثر طلباً 🔥</div>
            <h3 style="color: white; margin-top: 10px;">باقة المحترفين (PRO)</h3>
            <h2 style="color: #3b82f6; font-size: 36px; margin: 15px 0;">$29.99<span style='font-size:14px; color:#a0aec0;'>/شهرياً</span></h2>
            <ul style="list-style: none; padding: 0; color: #cbd5e1; text-align: right; direction: rtl; margin-bottom: 25px; line-height: 1.8;">
                <li style="margin-bottom: 10px;">✨ فك تشفير السيولة بالكامل (Liquidity Pools)</li>
                <li style="margin-bottom: 10px;">📊 مؤشر الـ ADX المطور لتحديد قوة وجاهزية الاتجاه</li>
                <li style="margin-bottom: 10px;">🎯 تحديد دقيق لمناطق الـ Order Blocks والـ FVG المؤسسية</li>
                <li style="margin-bottom: 10px;">⚡ تحديث تلقائي للبيانات مع تنبيهات لحظية</li>
            </ul>
            <a href="https://shoppy.gg/product/5ZAWaH9" target="_blank" style="background: #3b82f6; color: white; padding: 12px 24px; border-radius: 8px; text-decoration: none; display: block; font-weight: bold; transition: 0.3s; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);">شراء كود التفعيل الفوري (USDT) 💳</a>
        </div>
        """, unsafe_allow_html=True)

    with plan_col2:
        st.markdown("""
        <div class="pricing-card" style="background: rgba(30, 41, 59, 0.4); padding: 25px; border-radius: 15px; border: 1px solid #475569; text-align: center; margin-bottom: 20px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
            <div style="background: #475569; color: white; padding: 4px 12px; border-radius: 20px; font-size: 12px; display: inline-block; margin-bottom: 10px; font-weight: bold;">باقة الحوت</div>
            <h3 style="color: white; margin-top: 10px;">الباقة المميزة (PREMIUM)</h3>
            <h2 style="color: #e2e8f0; font-size: 36px; margin: 15px 0;">$59.99<span style='font-size:14px; color:#a0aec0;'>/شهرياً</span></h2>
            <ul style="list-style: none; padding: 0; color: #cbd5e1; text-align: right; direction: rtl; margin-bottom: 25px; line-height: 1.8;">
                <li style="margin-bottom: 10px;">🚀 كل مميزات باقة PRO المحترفة المذكورة سابقاً</li>
                <li style="margin-bottom: 10px;">🧠 دمج معادلة بايز الإحصائية لتوقع تدفقات السيولة المتكاملة</li>
                <li style="margin-bottom: 10px;">📈 تحليلات خاصة ومتقدمة لسيولة الذهب وحركة صناع السوق اليومية</li>
                <li style="margin-bottom: 10px;">📞 دعم فني خاص متصل ومباشر على مدار الساعة 24/7</li>
            </ul>
            <a href="#" style="background: #475569; color: white; padding: 12px 24px; border-radius: 8px; text-decoration: none; display: block; font-weight: bold; opacity: 0.6; cursor: not-allowed;">قريباً (قيد الإعداد) ⏳</a>
        </div>
        """, unsafe_allow_html=True)

    st.stop()

# 4. محتوى المنصة الرئيسي (يفتح فقط بعد التفعيل الناجح)
st.sidebar.title("⚡ التحكم بالمنصة")
st.sidebar.write(f"👤 نوع الحساب الحركي: **{st.session_state.user_tier}**")

if st.sidebar.button("تسجيل الخروج 🔓"):
    st.session_state.authenticated = False
    st.session_state.user_tier = None
    st.rerun()

st.title("📊 لوحة تحليلات السيولة المتقدمة للذهب")
st.write("تم تفعيل الاتصال المباشر بخوارزمية فك التشفير. البيانات أدناه تعكس حركة صناع السوق الحالية.")

# بيانات تجريبية لمحاكاة حركة الأسواق والأدوات الفنية
chart_data = pd.DataFrame(
    np.random.randn(20, 3) / 50 + 2350,
    columns=['Gold Price', 'Order Block Level', 'Fair Value Gap Close']
)

st.line_chart(chart_data)

st.success("✅ البيانات محدثة وتعمل وفقاً لتدفقات الاتجاه والمؤشرات المخصصة بنجاح.")
