from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # 使用render_template函数来渲染并返回index.html
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)