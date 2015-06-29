import os
import re

from flask import Flask, request, render_template, make_response
app = Flask(__name__)

def get_current(proxy):
    pass

def change_current(proxy, behavior, **optns):
    print proxy, behavior, optns

@app.route("/", methods=['GET', 'POST'])
def flash():
    if request.method == 'POST':
        req = request.form.to_dict()
        behavior = req.pop('behavior')
        proxy = req.pop('proxy')
        change_current(proxy, behavior, **req)

    links = os.environ.get('links', '').split(',')
    links = [(l,
              ' -> '.join(re.search('composemonkey_(.+)_(.+)', l).groups()),
              get_current(l)) for l in links]

    return render_template('index.html', links=links)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2020, debug=True)
