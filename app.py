from flask import Flask, render_template

app = Flask(__name__)

# ホームページのルート
@app.route('/')
def calender():
    
    return render_template('calender.html')

if __name__ == '__main__':
    app.run(port=8080, debug=True)
