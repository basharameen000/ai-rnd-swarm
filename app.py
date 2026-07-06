import streamlit as st
import json
import pandas as pd
import os

# إعدادات الصفحة الأساسية
st.set_page_config(page_title="رادار الوكلاء الخارقين", page_icon="🛸", layout="wide")

# تصميم الهيدر (Header)
st.title("🛸 منصة استكشاف وكلاء الذكاء الاصطناعي")
st.markdown("""
<div style='background-color: #1e1e1e; padding: 15px; border-radius: 10px; margin-bottom: 25px; border-left: 5px solid #00ffcc;'>
    هذه المنصة تعمل كقاعدة بيانات حية. يتم تحديثها تلقائياً بواسطة <b>سرب من الوكلاء</b> الذين يمسحون منصات (GitHub, HuggingFace) يومياً لاستخراج أفضل الأدوات وتحليلها لك.
</div>
""", unsafe_allow_html=True)

DB_FILE = "database.json"

@st.cache_data
def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return pd.DataFrame(data)
        except:
            pass
    
    # أعمدة قاعدة البيانات في حال كانت فارغة
    return pd.DataFrame(columns=[
        "اسم الأداة", "التصنيف", "المصدر", "الملخص التنفيذي", "قرار السرب", "الرابط"
    ])

df = load_data()

if df.empty:
    st.info("⏳ قاعدة البيانات فارغة. ننتظر سرب الوكلاء لإنهاء جولتهم الأولى...")
else:
    # --- أدوات البحث والفلترة ---
    st.subheader("🔍 البحث والتصفية")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_term = st.text_input("ابحث عن اسم أداة أو وظيفة:")
    with col2:
        category_filter = st.selectbox("التصنيف:", ["الكل"] + list(df["التصنيف"].unique()))
    with col3:
        source_filter = st.selectbox("المصدر:", ["الكل"] + list(df["المصدر"].unique()))

    # تطبيق الفلاتر
    filtered_df = df.copy()
    if search_term:
        filtered_df = filtered_df[filtered_df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]
    if category_filter != "الكل":
        filtered_df = filtered_df[filtered_df["التصنيف"] == category_filter]
    if source_filter != "الكل":
        filtered_df = filtered_df[filtered_df["المصدر"] == source_filter]

    # --- عرض البيانات بتصميم جذاب ---
    st.subheader(f"📊 النتائج المتاحة ({len(filtered_df)})")
    
    # تنسيق الجدول
    st.dataframe(
        filtered_df,
        column_config={
            "الرابط": st.column_config.LinkColumn("🔗 اضغط للزيارة"),
            "قرار السرب": st.column_config.TextColumn("حكم السرب النهائي", help="هل تستحق الأداة التجربة بناءً على تحليل الوكلاء؟"),
        },
        hide_index=True,
        use_container_width=True,
        height=400
    )

st.markdown("---")
st.caption("📡 AI R&D Swarm System V2.0 - Powered by Advanced Autonomous Agents")
