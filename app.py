from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# حط رابط الـ Production URL تبع الـ n8n هون
N8N_WEBHOOK_URL = "https://sayafbd.app.n8n.cloud/webhook/e1f47c44-85e2-46d1-be84-094afb426652"

@app.route('/', methods=['GET', 'POST'])
def index():
    ai_response = None
    
    if request.method == 'POST':
        # بناخذ رسالة الطالب من الفورم اللي بالموقع
        student_msg = request.form.get('message')
        
        # بنجهزها وبنبعثها للـ n8n زي ما عملنا قبل شوي
        data = {"student_message": student_msg}
        try:
            response = requests.post(N8N_WEBHOOK_URL, json=data)
            ai_response = response.text  # هاد السطر السحري اللي كان ضايع!
            ai_response = ai_response.replace('**', '')
        except Exception as e:
            print("سبب المشكلة:", e)  # ضيف هاد السطر
            ai_response = "عذراً، صار في مشكلة بالاتصال مع الموجه الأكاديمي."

    # بنعرض الصفحة وبنبعث الرد إذا موجود
    return render_template('index.html', response=ai_response)

if __name__ == '__main__':
    app.run(debug=True)