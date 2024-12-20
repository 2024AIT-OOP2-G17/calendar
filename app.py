from flask import Flask, render_template
from routes import blueprints

app = Flask(__name__)

# 各Blueprintをアプリケーションに登録
for blueprint in blueprints:
    app.register_blueprint(blueprint)

# ホームページのルート
@app.route('/')
def calendar():
    
    return render_template('calendar.html')

if __name__ == '__main__':
    app.run(port=8080, debug=True)
