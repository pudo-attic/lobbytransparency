
from flask import Flask, request, Response
from flask import render_template

from datetime import datetime
import json

import sqlaload as sl
import SETTINGS

app = Flask(__name__)
engine = sl.connect(SETTINGS.ETL_URL)
representative = sl.get_table(engine, 'representative')
network_entity = sl.get_table(engine, 'network_entity')

class JSONEncoder(json.JSONEncoder):
    """ This encoder will serialize all entities that have a to_dict
    method by calling that method and serializing the result. """

    def encode(self, obj):
        if hasattr(obj, 'to_dict'):
            obj = obj.to_dict()
        return super(JSONEncoder, self).encode(obj)

    def default(self, obj):
        if hasattr(obj, 'as_dict'):
            return obj.as_dict()
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError("%r is not JSON serializable" % obj)


def jsonify(obj, status=200, headers=None):
    """ Custom JSONificaton to support obj.to_dict protocol. """
    jsondata = json.dumps(obj, cls=JSONEncoder)
    if 'callback' in request.args:
        jsondata = '%s(%s)' % (request.args.get('callback'), jsondata)
    return Response(jsondata, headers=headers,
                    status=status, mimetype='application/json')


@app.route('/')
def index():
    return render_template('neegame.html')


@app.route('/get')
def get():
    rep = sl.find_one(engine, representative, network_extracted=False)
    print rep
    return jsonify(rep)


@app.route('/reset')
def reset():
    sl.update(engine, representative, {}, {'network_extracted': False})
    return jsonify({'status': 'OK'})


@app.route('/save', methods=['POST'])
def save():
    etlId = request.form.get('representativeEtlId')
    matches = set(request.form.getlist('matches[]'))
    for match in matches:
        match = match.strip().strip(",").strip(";").strip(".").strip()
        sl.upsert(engine, network_entity, {'etlFingerPrint': match,
                                           'representativeEtlId': etlId},
                ['etlFingerPrint', 'representativeEtlId'])
    sl.upsert(engine, representative, {'etlId': etlId,
        'network_extracted': True}, ['etlId'])
    return jsonify({'status': 'OK'})

if __name__ == '__main__':
    app.run(port=5003, debug=True)
