import streamlit as st
import time
import random

# ─── Page Configuration ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="منصة مواهب",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── RTL + Custom Styling ─────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');

    * { font-family: 'Cairo', sans-serif !important; }

    .main { direction: rtl; text-align: right; }
    .block-container { direction: rtl; padding-top: 2rem; }

    /* Hero card */
    .hero-card {
        background: linear-gradient(135deg, #6C3DE8 0%, #9B59B6 50%, #C0392B 100%);
        border-radius: 24px;
        padding: 3rem 2rem;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 20px 60px rgba(108, 61, 232, 0.35);
    }
    .hero-card h1 { font-size: 3rem; font-weight: 900; margin: 0; }
    .hero-card p  { font-size: 1.2rem; opacity: 0.9; margin-top: 0.5rem; }

    /* Feature cards */
    .feature-row { display: flex; gap: 1rem; margin: 1.5rem 0; }
    .feature-card {
        flex: 1;
        background: white;
        border-radius: 16px;
        padding: 1.5rem 1rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(108, 61, 232, 0.12);
        border: 1px solid #EDE7FF;
    }
    .feature-card .icon { font-size: 2.2rem; margin-bottom: 0.5rem; }
    .feature-card h3 { font-size: 1rem; font-weight: 700; color: #1A1A2E; margin: 0; }
    .feature-card p  { font-size: 0.82rem; color: #666; margin: 0.3rem 0 0; }

    /* Pricing cards */
    .pricing-grid { display: flex; gap: 1rem; margin: 1.5rem 0; flex-wrap: wrap; }
    .pricing-card {
        flex: 1; min-width: 200px;
        background: white;
        border-radius: 20px;
        padding: 1.8rem 1.2rem;
        text-align: center;
        box-shadow: 0 6px 24px rgba(0,0,0,0.08);
        border: 2px solid #EDE7FF;
        transition: all 0.3s;
        cursor: pointer;
    }
    .pricing-card.popular {
        background: linear-gradient(135deg, #6C3DE8, #9B59B6);
        color: white;
        border-color: transparent;
        transform: scale(1.04);
        box-shadow: 0 12px 40px rgba(108, 61, 232, 0.4);
    }
    .pricing-card .badge {
        background: #FFD700;
        color: #1A1A2E;
        border-radius: 20px;
        padding: 2px 12px;
        font-size: 0.75rem;
        font-weight: 700;
        display: inline-block;
        margin-bottom: 0.7rem;
    }
    .pricing-card .plan-name { font-size: 1.1rem; font-weight: 700; margin-bottom: 0.5rem; }
    .pricing-card .plan-price { font-size: 2.2rem; font-weight: 900; margin: 0.5rem 0; }
    .pricing-card .plan-period { font-size: 0.85rem; opacity: 0.75; }
    .pricing-card ul { list-style: none; padding: 0; margin: 1rem 0 0; text-align: right; }
    .pricing-card ul li { padding: 0.25rem 0; font-size: 0.85rem; }
    .pricing-card ul li::before { content: "✓  "; color: #6C3DE8; font-weight: 700; }
    .pricing-card.popular ul li::before { color: #FFD700; }

    /* Step indicator */
    .step-bar { display: flex; justify-content: center; gap: 0.5rem; margin-bottom: 2rem; }
    .step-dot {
        width: 12px; height: 12px; border-radius: 50%;
        background: #DDD;
        transition: background 0.4s;
    }
    .step-dot.active { background: #6C3DE8; }
    .step-dot.done   { background: #9B59B6; }

    /* Loading steps */
    .load-step {
        display: flex; align-items: center; gap: 0.8rem;
        padding: 0.8rem 1.2rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        background: white;
        border: 1px solid #EDE7FF;
        font-size: 0.95rem;
        direction: rtl;
    }
    .load-step.done { border-color: #6C3DE8; background: #F0EBFF; }
    .load-step.active { border-color: #9B59B6; background: #FDF5FF; animation: pulse 1s infinite; }

    @keyframes pulse {
        0%, 100% { box-shadow: 0 0 0 0 rgba(108, 61, 232, 0.3); }
        50%       { box-shadow: 0 0 0 6px rgba(108, 61, 232, 0); }
    }

    /* General */
    .section-title {
        font-size: 1.6rem; font-weight: 800;
        color: #1A1A2E; text-align: center;
        margin: 1.5rem 0 1rem;
    }
    .subtitle {
        text-align: center; color: #666;
        font-size: 1rem; margin-bottom: 2rem;
    }

    /* Hide Streamlit branding */
    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)

# ─── Session State Init ────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "landing"
if "idea" not in st.session_state:
    st.session_state.idea = ""
if "selected_plan" not in st.session_state:
    st.session_state.selected_plan = "شامل"
if "paid" not in st.session_state:
    st.session_state.paid = False


def go_to(page):
    st.session_state.page = page
    st.rerun()


# ─── Step Indicator ────────────────────────────────────────────────────────────
def step_indicator(current):
    steps = ["landing", "idea", "loading", "pricing"]
    dots = ""
    for s in steps:
        if s == current:
            dots += '<div class="step-dot active"></div>'
        elif steps.index(s) < steps.index(current):
            dots += '<div class="step-dot done"></div>'
        else:
            dots += '<div class="step-dot"></div>'
    st.markdown(f'<div class="step-bar">{dots}</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 1 — LANDING
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "landing":

    step_indicator("landing")

    st.markdown("""
    <div class="hero-card">
        <div style="font-size:3.5rem; margin-bottom:0.5rem;">🚀</div>
        <h1>منصة مواهب</h1>
        <p>حوّل فكرتك إلى مشروع رقمي متكامل بقوة الذكاء الاصطناعي<br>
        وادفع تكاليف التطوير بالتقسيط المريح</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-row">
        <div class="feature-card">
            <div class="icon">🤖</div>
            <h3>توليد بالذكاء الاصطناعي</h3>
            <p>المنصة تحلل فكرتك وتبني خطة المشروع كاملة خلال ثوانٍ</p>
        </div>
        <div class="feature-card">
            <div class="icon">💳</div>
            <h3>تقسيط BNPL</h3>
            <p>ادفع الآن واحصل على مشروعك — سدّد لاحقاً بأقساط مرنة</p>
        </div>
        <div class="feature-card">
            <div class="icon">⚡</div>
            <h3>تسليم سريع</h3>
            <p>من الفكرة إلى التسليم في أقل وقت ممكن</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀  ابدأ مشروعك الآن", use_container_width=True, type="primary"):
            go_to("idea")

    st.markdown("""
    <p style="text-align:center; color:#999; margin-top:1.5rem; font-size:0.85rem;">
    انضم إلى +2,000 رائد أعمال يستخدمون منصة مواهب
    </p>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 2 — IDEA INPUT
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "idea":

    step_indicator("idea")

    st.markdown('<div class="section-title">💡 أخبرنا عن فكرتك</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">صِف مشروعك بكلماتك — الذكاء الاصطناعي سيتولى الباقي</div>', unsafe_allow_html=True)

    idea_text = st.text_area(
        label="فكرة مشروعك",
        placeholder="مثال: أريد تطبيق لتوصيل الطلبات بين المطاعم والعملاء في مدينتي، يشمل تتبع الطلب لحظياً، نظام تقييم، ولوحة تحكم للمطاعم...",
        height=180,
        key="idea_input",
        label_visibility="collapsed",
    )

    st.markdown("---")

    col_back, col_space, col_next = st.columns([1, 2, 1])
    with col_back:
        if st.button("⬅️ رجوع", use_container_width=True):
            go_to("landing")
    with col_next:
        if st.button("✨ ولّد مشروعي", use_container_width=True, type="primary"):
            if idea_text.strip():
                st.session_state.idea = idea_text.strip()
                go_to("loading")
            else:
                st.warning("⚠️ الرجاء كتابة فكرة مشروعك أولاً")

    st.markdown("""
    <div style="background:#F0EBFF; border-radius:14px; padding:1rem 1.2rem; margin-top:1.5rem; direction:rtl;">
        <b>💬 نصيحة:</b> كلما كانت فكرتك أكثر تفصيلاً، كان المشروع المُولَّد أدق وأشمل.
        اذكر الجمهور المستهدف، المميزات الأساسية، والمشكلة التي يحلها مشروعك.
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 3 — SMART LOADING
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "loading":

    step_indicator("loading")

    st.markdown('<div class="section-title">🧠 الذكاء الاصطناعي يعمل...</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle">جاري تحليل فكرتك وبناء مشروعك المثالي</div>', unsafe_allow_html=True)

    if st.session_state.idea:
        st.markdown(f"""
        <div style="background:#EDE7FF; border-right:4px solid #6C3DE8;
                    border-radius:12px; padding:0.8rem 1rem; margin-bottom:1.5rem;
                    direction:rtl; font-size:0.9rem; color:#333;">
            💡 <b>فكرتك:</b> {st.session_state.idea[:150]}{"..." if len(st.session_state.idea) > 150 else ""}
        </div>
        """, unsafe_allow_html=True)

    # Build loading steps
    ai_steps = [
        ("🔍", "تحليل الفكرة وتحديد نطاق المشروع"),
        ("🏗️", "تصميم هيكل المشروع والصفحات"),
        ("🎨", "اختيار الألوان والهوية البصرية"),
        ("⚙️", "تحديد التقنيات والأدوات المناسبة"),
        ("📋", "إعداد خطة التطوير والجدول الزمني"),
        ("💰", "احتساب التكاليف وخيارات التقسيط"),
        ("✅", "مراجعة النتائج وإعداد التقرير النهائي"),
    ]

    progress_bar = st.progress(0)
    steps_container = st.empty()

    completed = []
    for i, (icon, label) in enumerate(ai_steps):
        # Render steps
        steps_html = ""
        for j, (ic, lb) in enumerate(ai_steps):
            if j < i:
                cls = "done"
                status_icon = "✅"
            elif j == i:
                cls = "active"
                status_icon = "⏳"
            else:
                cls = ""
                status_icon = "⬜"
            steps_html += f'<div class="load-step {cls}">{status_icon} {ic} {lb}</div>'

        steps_container.markdown(steps_html, unsafe_allow_html=True)
        progress_bar.progress(int((i + 1) / len(ai_steps) * 100))
        time.sleep(random.uniform(0.55, 0.95))

    # Final state
    steps_html = "".join(
        f'<div class="load-step done">✅ {ic} {lb}</div>'
        for ic, lb in ai_steps
    )
    steps_container.markdown(steps_html, unsafe_allow_html=True)
    progress_bar.progress(100)
    time.sleep(0.5)

    st.success("🎉 تم توليد مشروعك بنجاح! شاهد باقات التقسيط المتاحة لك")
    time.sleep(1.2)
    go_to("pricing")


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 4 — PRICING / BNPL
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "pricing":

    step_indicator("pricing")

    if not st.session_state.paid:

        st.markdown('<div class="section-title">🎊 مشروعك جاهز! اختر باقة التقسيط</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">ادفع الآن أو قسّط بدون فوائد — المشروع يُسلَّم فور التأكيد</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="pricing-grid">
            <div class="pricing-card">
                <div class="plan-name">⚡ الباقة السريعة</div>
                <div class="plan-price">4,999 ر.س</div>
                <div class="plan-period">دفعة واحدة — توفير 10%</div>
                <ul>
                    <li>تطبيق ويب كامل</li>
                    <li>تصميم احترافي</li>
                    <li>تسليم خلال 30 يوم</li>
                    <li>3 أشهر دعم فني</li>
                </ul>
            </div>
            <div class="pricing-card popular">
                <div class="badge">⭐ الأكثر طلباً</div>
                <div class="plan-name">🚀 الباقة الشاملة</div>
                <div class="plan-price">1,799 ر.س</div>
                <div class="plan-period">شهرياً / 3 أشهر — بدون فوائد</div>
                <ul>
                    <li>كل ما في السريعة</li>
                    <li>تطبيق جوال iOS & Android</li>
                    <li>لوحة تحكم متقدمة</li>
                    <li>6 أشهر دعم فني</li>
                    <li>تدريب الفريق</li>
                </ul>
            </div>
            <div class="pricing-card">
                <div class="plan-name">💎 الباقة المميزة</div>
                <div class="plan-price">999 ر.س</div>
                <div class="plan-period">شهرياً / 6 أشهر — بدون فوائد</div>
                <ul>
                    <li>كل ما في الشاملة</li>
                    <li>ذكاء اصطناعي متكامل</li>
                    <li>تحليلات متقدمة</li>
                    <li>سنة كاملة دعم فني</li>
                    <li>أولوية في التطوير</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        selected = st.radio(
            "اختر الباقة المناسبة لك:",
            options=["⚡ الباقة السريعة — 4,999 ر.س (دفعة واحدة)", "🚀 الباقة الشاملة — 1,799 ر.س/شهر × 3", "💎 الباقة المميزة — 999 ر.س/شهر × 6"],
            index=1,
            key="plan_radio",
        )

        plan_map = {
            "⚡ الباقة السريعة — 4,999 ر.س (دفعة واحدة)": ("4,999 ر.س", "دفعة واحدة"),
            "🚀 الباقة الشاملة — 1,799 ر.س/شهر × 3":      ("1,799 ر.س", "لمدة 3 أشهر"),
            "💎 الباقة المميزة — 999 ر.س/شهر × 6":         ("999 ر.س",  "لمدة 6 أشهر"),
        }
        amount, period = plan_map[selected]

        st.markdown(f"""
        <div style="background:#F0EBFF; border-radius:14px; padding:1rem 1.2rem;
                    direction:rtl; margin: 1rem 0;">
            <b>📝 ملخص طلبك:</b><br>
            الباقة المختارة: <b>{selected.split('—')[0].strip()}</b><br>
            المبلغ: <b>{amount}</b> {period}<br>
            طريقة الدفع: <b>BNPL — بدون فوائد</b>
        </div>
        """, unsafe_allow_html=True)

        col_back, col_space, col_pay = st.columns([1, 1, 2])
        with col_back:
            if st.button("⬅️ رجوع", use_container_width=True):
                go_to("idea")
        with col_pay:
            if st.button(f"💳  ادفع الآن — {amount}", use_container_width=True, type="primary"):
                st.session_state.paid = True
                st.rerun()

        st.markdown("""
        <div style="text-align:center; margin-top:1.5rem; color:#999; font-size:0.82rem;">
            🔒 مدفوعات آمنة 100% &nbsp;|&nbsp; بدون فوائد &nbsp;|&nbsp; يمكنك الإلغاء في أي وقت
        </div>
        """, unsafe_allow_html=True)

    else:
        # ── SUCCESS SCREEN ────────────────────────────────────────────────────
        st.balloons()

        st.markdown("""
        <div class="hero-card" style="background: linear-gradient(135deg, #27AE60 0%, #2ECC71 100%);">
            <div style="font-size:4rem;">🎉</div>
            <h1 style="font-size:2.2rem;">تم الدفع بنجاح!</h1>
            <p>مبروك! انطلق مشروعك رسمياً — فريقنا سيتواصل معك خلال 24 ساعة</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-row">
            <div class="feature-card">
                <div class="icon">📧</div>
                <h3>تأكيد بالبريد</h3>
                <p>ستصلك رسالة تأكيد على بريدك الإلكتروني</p>
            </div>
            <div class="feature-card">
                <div class="icon">👨‍💻</div>
                <h3>تخصيص مدير</h3>
                <p>سيتم تعيين مدير مشروع متخصص لمتابعتك</p>
            </div>
            <div class="feature-card">
                <div class="icon">📅</div>
                <h3>جدول التسليم</h3>
                <p>ستتلقى جدول تسليم مفصل خلال 24 ساعة</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🏠  العودة للصفحة الرئيسية", use_container_width=True, type="primary"):
                st.session_state.page = "landing"
                st.session_state.paid = False
                st.session_state.idea = ""
                st.rerun()
