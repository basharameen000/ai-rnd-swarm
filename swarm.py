import os
import json
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from langchain.tools import tool
import requests

# ==========================================
# 0. إعداد محرك KILO (OpenAI Compatible)
# ==========================================
# ميزة منصات مثل Kilo أو OpenRouter أنها متوافقة 100% مع كود OpenAI
# لذلك نحن نستخدم مكتبة OpenAI ولكن نوجهها لسيرفرات Kilo!

KILO_API_KEY = os.environ.get("KILO_API_KEY", "ضع_مفتاح_kilo_هنا")

# نستخدم واجهة OpenAI لكن نخدعها لتتصل بـ Kilo
llm = ChatOpenAI(
    model="llama-3-70b-instruct", # يمكنك تغييره لأي نموذج متوفر في Kilo
    api_key=KILO_API_KEY,
    base_url="https://api.kilo.com/v1" # هذا الرابط القياسي، يمكن تعديله حسب توثيق منصتك
)

# ==========================================
# 1. أدوات الاستخراج المخصصة (Custom Scrapers)
# ==========================================

@tool("HuggingFace_Trending_Scraper")
def scrape_huggingface() -> str:
    """تستخدم لجلب أحدث وأقوى النماذج مفتوحة المصدر والوكلاء من HuggingFace."""
    # (محاكاة ذكية للاتصال بالـ API الحقيقي)
    return "تم العثور على: 1. SmolAgents (مكتبة وكلاء). 2. Qwen2.5-Coder (نموذج برمجة)."

@tool("GitHub_Trending_Scraper")
def scrape_github() -> str:
    """تستخدم لجلب أحدث أدوات المطورين ووكلاء الذكاء الاصطناعي من GitHub Trending."""
    # (محاكاة ذكية للاتصال بالـ API الحقيقي)
    return "تم العثور على: 1. OpenHands (وكيل هندسة برمجيات مستقل). 2. CrewAI (تحديث جديد)."

# ==========================================
# 2. بناء الوكلاء (Agents)
# ==========================================

scout = Agent(
    role='وكيل الاستخراج الاستخباراتي',
    goal='جلب أحدث وأقوى وكلاء ونماذج الذكاء الاصطناعي من مصادر المطورين الموثوقة حصراً.',
    backstory='أنت مستكشف تقني محترف. تعتمد فقط على المصادر الموثوقة للمطورين ولا تضيع وقتك في محركات البحث العادية.',
    verbose=True,
    allow_delegation=False,
    tools=[scrape_huggingface, scrape_github],
    llm=llm
)

analyst = Agent(
    role='المحلل الفني الصارم',
    goal='تحليل الأدوات المستخرجة، وتحديد ما إذا كانت قوية فعلاً وتستحق الإضافة لمنصة المستخدم.',
    backstory='أنت مهندس برمجيات لا يقتنع بسهولة. وظيفتك هي إزالة "وهم التسويق" وتحديد الفائدة الحقيقية للأداة.',
    verbose=True,
    allow_delegation=False,
    llm=llm
)

db_manager = Agent(
    role='مدير قاعدة البيانات (Database Engineer)',
    goal='تحويل تحليلات السرب إلى تنسيق JSON دقيق ومطابق لهيكلية واجهة Streamlit ليتم عرضه مباشرة.',
    backstory='أنت مهندس بيانات دقيق جداً. وظيفتك الوحيدة هي أخذ النصوص المكتوبة وتحويلها إلى كود JSON منظم بدون أي نصوص إضافية.',
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# ==========================================
# 3. تحديد المهام (Tasks)
# ==========================================

task1 = Task(
    description='استخدم أدواتك للبحث في HuggingFace و GitHub عن أحدث وكلاء الذكاء الاصطناعي.',
    expected_output='قائمة بالأدوات المكتشفة مع مصادرها.',
    agent=scout
)

task2 = Task(
    description='بناءً على قائمة وكيل الاستخراج، اكتب تقييماً فنياً مختصراً لكل أداة وهل تنصح بها.',
    expected_output='تحليل فني قصير لكل أداة مع قرار بمدى جودتها.',
    agent=analyst
)

task3 = Task(
    description='''
    خذ التحليل النهائي، وقم بتحويله إلى تنسيق JSON Array.
    يجب أن يحتوي كل عنصر على الحقول التالية بالضبط:
    "اسم الأداة", "التصنيف", "المصدر", "الملخص التنفيذي", "قرار السرب", "الرابط".
    هام جداً: لا تكتب أي كلمة أخرى غير كود الـ JSON، حتى أستطيع حفظه في قاعدة البيانات.
    ''',
    expected_output='كود JSON صحيح بنسبة 100% يمثل قاعدة البيانات.',
    agent=db_manager
)

# ==========================================
# 4. محرك السرب (Crew Kickoff)
# ==========================================

ai_rnd_crew = Crew(
    agents=[scout, analyst, db_manager],
    tasks=[task1, task2, task3],
    process=Process.sequential,
    verbose=True
)

if __name__ == "__main__":
    print("🚀 بدء عمل السرب السحابي (محرك KILO)...")
    result = ai_rnd_crew.kickoff()
    
    # تحديث قاعدة البيانات التي تقرأ منها واجهة الويب
    try:
        raw_text = result.raw if hasattr(result, 'raw') else str(result)
        # تنظيف النص تحسباً لوجود أي علامات Markdown
        cleaned_json = raw_text.replace("```json", "").replace("```", "").strip()
        new_data = json.loads(cleaned_json)
        
        with open("database.json", "w", encoding="utf-8") as f:
            json.dump(new_data, f, ensure_ascii=False, indent=2)
        print("✅ تم تحديث قاعدة بيانات المنصة (database.json) بنجاح!")
    except Exception as e:
        print("❌ حدث خطأ في معالجة مخرجات السرب:", e)
