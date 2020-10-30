from flask import Flask, render_template

app = Flask(__name__)

@app.route('/', methods=('GET',))
def home():
    return render_template('startside.html')


@app.route('/layout', methods=('GET', 'POST'))
def layout():
    return render_template('layout.html')


if __name__ == '__main__':
    app.run()