from flask import Flask, jsonify

from src.database.sqlite_opt import sqlite_opt

app = Flask(__name__)


@app.route('/')
def index():
    """主页
    """
    return '''
        ok
    '''


@app.route('/get')
def get_proxy():
    proxy = sqlite_opt.get_one_in_page()
    if proxy:
        return jsonify({
            'code': 200,
            'proxy': proxy.url
        })
    else:
        return jsonify({'code': 500, 'msg': 'server error'})


@app.route('/get_all')
def get_all_proxy():
    proxy_list = sqlite_opt.get_all_in_page()
    if proxy_list:
        return jsonify({
            'code': 200,
            'proxies': [proxy.url for proxy in proxy_list]
        })
    else:
        return jsonify({'code': 500, 'msg': 'server error'})
