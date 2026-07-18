import streamlit as st
import time

# إعدادات الصفحة العامة (يجب أن تكون أول أمر من streamlit)
st.set_page_config(
    page_title="منصة مواهب - توليد وتقسيط المشاريع بالذكاء الاصطناعي",
    page_icon="💡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# تفعيل التصميم العربي (RTL) وتحسين المظهر عبر CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap');
    
    html, body, [data-testid="stSidebarViewPort"], .main {
        font-family: 'Tajawal', sans-serif;
        direction: RTL;
        text-align: right;
    }
    div[data-testid="stMarkdownContainer"] > p {
        text-align: right;
    }
    .stButton>button {
        width: 100%;
        font-family: 'Tajawal', sans-serif;
        background-color: #2e7d32;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-size: 1.1rem;
    }
    .stButton>button:hover {
        background-color: #1b5e20;
        color: white;
    }
    .card {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #f8f9fa;
        border-right: 5px solid #2e7d32;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .price-card {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #ffffff;
        border: 2px solid #e0e0e0;
        text-align: center;
        margin-bottom: 1rem;
    }
    .price-card.selected {
        border-color: #2e7d32;
        background-color: #f1f8e9;
    }
    </style>
""", unsafe_allow_html=True)

# إدارة حالة الشاشات والتنقل (Session State)
if 'step' not in st.session_state:
    st.session_state.step = 'landing'
if 'user_idea' not in st.session_state:
    st.session_state.user_idea = ""
if 'selected_plan' not in st.session_state:
    st.session_state.selected_plan = None

# --- 1. صفحة الهبوط ---
if st.session_state.step == 'landing':
    st.title("💡 منصة مواهب")
    st.subheader("حوّل فكرتك إلى مشروع متكامل بدعم الذاء الاصطناعي.. وابدأ الدفع بالتقسيط!")
    
    st.markdown("""
    <div class="card">
        <h3>🚀 لماذا منصة مواهب؟</h3>
        <p>نحن ندمج بين قوة الذكاء الاصطناعي التوليدي والحلول المالية الذكية. اكتب فكرتك فقط، وسنقوم بتوليد خطة العمل، الهوية البصرية، والبرمجة الأولية، مع إمكانية تقسيط التكاليف بالكامل بنظام (اشترِ الآن وادفع لاحقاً - BNPL).</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    if st.button("ابدأ رحلتك الآن وتوليد مشروعك ➔"):
        st.session_state.step = 'input_idea'
        st.rerun()

# --- 2. شاشة كتابة الفكرة ---
elif st.session_state.step == 'input_idea':
    st.title("📝 اخبرنا عن فكرتك")
    st.write("اكتب وصفاً مبسطاً للمشروع الذي تطمح لتأسيسه، وسيتولى الذكاء الاصطناعي الباقي.")
    
    idea = st.text_area("وصف الفكرة:", placeholder="مثال: تطبيق لتوصيل الوجبات الصحية السريعة للاعبي الرياضة بأسعار مناسبة...", height=150)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("العودة"):
            st.session_state.step = 'landing'
            st.rerun()
    with col2:
        if st.button("توليد المشروع باستخدام AI ✨"):
            if idea.strip() == "":
                st.error("الرجاء كتابة فكرتك أولاً لنتمكن من تحليلها!")
            else:
                st.session_state.user_idea = idea
                st.session_state.step = 'loading'
                st.rerun()

# --- 3. شاشة التحميل الذكية ---
elif st.session_state.step == 'loading':
    st.title("🤖 جاري تحليل وتوليد مشروعك...")
    st.write("يقوم الذكاء الاصطناعي الآن ببناء الهوية وخطة العمل الافتراضية لفكرتك:")
    st.info(f"💡 الفكرة الحالية: {st.session_state.user_idea}")
    
    # محاكاة خطوات التوليد الذكي عبر شريط تقدم ونصوص متغيرة
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    steps = [
        "🔍 جاري تحليل دراسة الجدوى والسوق المستهدف...",
        "🎨 جاري ابتكار الهوية البصرية والشعار المقترح...",
        "💻 جاري بناء الهيكلية البرمجية للمنصة والميكروخدمات...",
        "📊 جاري حساب التكاليف التشغيلية وإعداد باقات التقسيط المناسبة..."
    ]
    
    for i, step_msg in enumerate(steps):
        status_text.markdown(f"**{step_msg}**")
        for percent in range(i * 25, (i + 1) * 25):
            time.sleep(0.03)
            progress_bar.progress(percent + 1)
            
    status_text.success("✅ تم توليد تفاصيل المشروع بنجاح!")
    time.sleep(1)
    st.session_state.step = 'pricing'
    st.rerun()

# --- 4. شاشة باقات التقسيط والدفع ---
elif st.session_state.step == 'pricing':
    st.title("💳 اختر باقة التقسيط المناسبة لمشروعك")
    st.write("تم احتساب تكاليف التوليد والتشغيل، يمكنك الاختيار بين خطط التقسيط المرنة بنظام (BNPL):")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="price-card">
            <h4>باقة الانطلاق</h4>
            <h3>250 ريال <small>/ شهر</small></h3>
            <p>مقسطة على 4 أشهر</p>
            <hr>
            <p>شاملة الهوية وخطة العمل</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("اختيار باقة الانطلاق"):
            st.session_state.selected_plan = "باقة الانطلاق (250 ريال/شهر)"
            
    with col2:
        st.markdown("""
        <div class="price-card" style="border-color: #2e7d32; background-color: #f1f8e9;">
            <h4>باقة النمو (الموصى بها)</h4>
            <h3>500 ريال <small>/ شهر</small></h3>
            <p>مقسطة على 6 أشهر</p>
            <hr>
            <p>شاملة تطبيق أولي + لوحة تحكم</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("اختيار باقة النمو"):
            st.session_state.selected_plan = "باقة النمو (500 ريال/شهر)"
            
    with col3:
        st.markdown("""
        <div class="price-card">
            <h4>الباقة المتكاملة</h4>
            <h3>900 ريال <small>/ شهر</small></h3>
            <p>مقسطة على 6 أشهر</p>
            <hr>
            <p>تطبيق كامل + دعم فني وسحابي</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("اختيار الباقة المتكاملة"):
            st.session_state.selected_plan = "الباقة المتكاملة (900 ريال/شهر)"

    st.write("---")
    
    if st.session_state.selected_plan:
        st.success(f"الباقة المختارة حالياً: **{st.session_state.selected_plan}**")
        
        st.subheader("🔒 إتمام عملية الدفع (محاكاة)")
        cc_col1, cc_col2 = st.columns(2)
        with cc_col1:
            st.text_input("رقم البطاقة", "4000 1234 5678 9010", disabled=True)
        with cc_col2:
            st.text_input("الاسم على البطاقة", "MOHAMMED AL-AHMADI", disabled=True)
            
        if st.button("💳 تأكيد تقسيط الدفعة الأولى وتفعيل المشروع"):
            st.balloons()
            st.success("🎉 تهانينا! تم اعتماد خطة التقسيط وبدء تشغيل مشروعك بنجاح. بالتوفيق في المسابقة!")
            if st.button("ابدأ من جديد"):
                st.session_state.step = 'landing'
                st.session_state.selected_plan = None
                st.rerun()
    else:
        st.info("الرجاء الضغط على زر اختيار الباقة المطلوبة لتفعيل خيارات الدفع والتقسيط.")
        
    if st.button("⬅️ تعديل فكرة المشروع"):
        st.session_state.step = 'input_idea'
        st.session_state.selected_plan = None
        st.rerun()