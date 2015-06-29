import os
import re

import json
import requests
from flask import Flask, request, render_template, make_response
app = Flask(__name__)

def get_current(proxy):
    return requests.get('http://{0}:2020/behavior'.format(proxy)).json()['behavior']

def change_current(proxy, behavior, **optns):
    requests.put('http://{0}:2020/behavior'.format(proxy),
                 data=json.dumps(optns))

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
