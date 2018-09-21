from flask import Flask, request

app = Flask(__name__)

@app.route('/',methods=['GET', 'POST'])
def knock_knock():
    res = 'hello'
    if request.method == 'POST':
        res = 'hi'
    return res


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)