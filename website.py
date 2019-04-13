import json

from flask import Flask, render_template, request
from flask.json import jsonify

import config
from utils.db_tool import MysqlConn

app = Flask(__name__)
mysql_conn = m_conn = MysqlConn(config.DB_HOST,
                                config.DB_PORT,
                                config.DB_USER,
                                config.DB_PASSWORD,
                                config.DB_NAME)


@app.route("/")
def hello():
    return render_template('index.html')


@app.route('/data')
def get_data():
    name = request.args.get('name', '')
    sort = request.args.get('sort', 'p_id')
    order = request.args.get('order', 'asc')
    limit = int(request.args.get('limit', '10'))
    offset = int(request.args.get('offset', '1'))
    result, total = mysql_conn.select_phone(name, sort, order, limit, offset)
    data = {
        'msg': '查询成功',
        'suc': True,
        'res': result,
        'total': total
    }
    return jsonify(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
