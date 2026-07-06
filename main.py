import os
from crewai import Agent, Task, Crew, Process
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_openai import ChatOpenAI

# إعداد نموذج اللغة (نستخدم هنا OpenAI كمثال قياسي، يتطلب مفتاح API)
# ملاحظة: يمكنك لاحقاً استبداله بنماذج أخرى مجانية أو محلية إذا أردت.
os.environ["OPENAI_API_KEY"] = "ضع_مفتاح_الـ_API_الخاص_بك_هنا"
llm = ChatOpenAI(model="gpt-4o")

# أداة البحث في الإنترنت (مجانية ومفتوحة)
search_tool = DuckDuckGoSearchRun()

# ==========================================
# 1. بناء الوكلاء (Agents Definition)
# ==========================================

scout = Agent(
    role='وكيل الاستطلاع (Scout Agent)',
    goal='البحث المستمر عن أحدث أدوات ووكلاء الذكاء الاصطناعي (AI Agents) التي ظهرت مؤخراً.',
    backstory='أنت خبير تقني شغوف بمتابعة أحدث التقنيات. وظيفتك هي مراقبة الإنترنت والعثور على الأدوات الجديدة قبل أن تصبح مشهورة.',
    verbose=True,
    allow_delegation=False,
    tools=[search_tool],
    llm=llm
)

analyst = Agent(
    role='وكيل التحليل (Analyst Agent)',
    goal='تحليل أدوات الذكاء الاصطناعي المكتشفة، فهم قدراتها الحقيقية، وإزالة وهم التسويق.',
    backstory='أنت مهندس برمجيات متشكك ومحلل تقني بارع. أنت لا تنخدع بالكلمات التسويقية. وظيفتك هي البحث عن التوثيق (Docs) ومعرفة ما يمكن للأداة فعله حقاً، وما هي قيودها.',
    verbose=True,
    allow_delegation=False,
    tools=[search_tool],
    llm=llm
)

synthesizer = Agent(
    role='وكيل التلخيص التنفيذي (Synthesizer Agent)',
    goal='صياغة تقرير تنفيذي قصير ومباشر باللغة العربية يوضح الخلاصة النهائية للمستخدم.',
    backstory='أنت مستشار تنفيذي ممتاز في إيصال المعلومات المعقدة بشكل بسيط ومباشر. أنت تعرف أن وقت مديرك ثمين جداً وتقدم له "الزبدة" فقط.',
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# ==========================================
# 2. تحديد المهام (Tasks Definition)
# ==========================================

task1 = Task(
    description='ابحث في الإنترنت عن أحدث 3 أدوات أو وكلاء ذكاء اصطناعي (Autonomous AI Agents) تم إطلاقها أو تصدرت التريند هذا الأسبوع. اجمع روابطهم ووصفاً مبدئياً عنهم.',
    expected_output='قائمة بـ 3 أدوات ذكاء اصطناعي جديدة مع روابطها ووصف مبدئي.',
    agent=scout
)

task2 = Task(
    description='بناءً على الأدوات التي وجدها وكيل الاستطلاع، قم بتحليل كل أداة بعمق. ابحث عن ميزاتها الحقيقية، وهل هي مفتوحة المصدر، وما هي المشكلة الدقيقة التي تحلها.',
    expected_output='تحليل فني دقيق لكل أداة يوضح قدراتها الحقيقية، وهل تستحق وقت المستخدم.',
    agent=analyst
)

task3 = Task(
    description='بناءً على التحليل الفني، اكتب تقريراً تنفيذياً باللغة العربية. التقرير يجب أن يحتوي لكل أداة على: اسم الأداة، ماذا تفعل (في سطر واحد)، وهل تنصح بتجربتها أم لا ولماذا.',
    expected_output='تقرير تنفيذي نهائي باللغة العربية بأسلوب احترافي، منظم ومباشر.',
    agent=synthesizer
)

# ==========================================
# 3. تكوين محرك السرب (Form the Crew)
# ==========================================

ai_rnd_crew = Crew(
    agents=[scout, analyst, synthesizer],
    tasks=[task1, task2, task3],
    process=Process.sequential, # المهام تعمل بشكل متسلسل
    verbose=True
)

# ==========================================
# 4. بدء التشغيل (Execution)
# ==========================================
if __name__ == "__main__":
    print("🚀 بدء عمل سرب البحث والتطوير (AI R&D Swarm)... الرجاء الانتظار.")
    result = ai_rnd_crew.kickoff()
    
    print("\n==========================================")
    print("✅ التقرير النهائي جاهز:")
    print("==========================================")
    print(result)

    # حفظ التقرير في ملف Markdown
    with open('dashboard_report.md', 'w', encoding='utf-8') as f:
        # التعامل مع الكائن المرتجع بناءً على إصدار CrewAI
        output_text = result.raw if hasattr(result, 'raw') else str(result)
        f.write("# تقرير الرادار لأدوات الذكاء الاصطناعي\n\n")
        f.write(output_text)
    print("\n💾 تم حفظ التقرير في ملف dashboard_report.md")
