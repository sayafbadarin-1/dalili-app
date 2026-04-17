from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os

app = Flask(__name__)

# جلب المفتاح السري (رح نحطه في Vercel كمان شوي)
API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

# إعداد البوت والتعليمات الصارمة (النظام الأمني والتوجيهي)
system_instruction = """
أنت 'دليلي'، موجه أكاديمي ذكي للطلاب.
يجب عليك الالتزام بالقواعد التالية حرفياً:
1. إذا سألك الطالب سؤالاً أكاديمياً أو طلب خطة دراسية: أعطه خطة دراسية عملية ومباشرة من 3 خطوات فقط، متبوعة باختبار قصير (Quiz) من 3 أسئلة للتأكد من فهمه.
2. إذا سألك أي سؤال خارج نطاق التعليم والدراسة، أو استخدم كلمات غير لائقة: ارفض الإجابة بلطف وقل فقط: 'عذراً، أنا مخصص للمساعدة الأكاديمية والدراسية فقط. كيف يمكنني مساعدتك في دراستك اليوم؟'
"""

# تجهيز الموديل
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_instruction
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"response": "يرجى كتابة رسالة."})
        
    try:
        # إرسال رسالة الطالب لـ Gemini
        response = model.generate_content(user_message)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"response": "عذراً، حدث خطأ في الاتصال. يرجى المحاولة مرة أخرى."})

if __name__ == '__main__':
    app.run(debug=True)
