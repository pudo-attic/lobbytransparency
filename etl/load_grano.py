import sqlaload as sl

from granoclient import GranoClient

import SETTINGS
from schema import *


def entity_upsert(session, collection, obj, *keys):
    query = [k + ':' + obj[k] for k in keys]
    res = session.get(session.api + '/' + collection,
            params={'limit': 1, 'filter': query,
                    'type': obj['type']})
    matches = json.loads(res.text)
    data = json.dumps(obj)
    if matches:
        res = session.put(session.api + '/' + collection + '/' + matches[0]['id'],
            data=data)
        assert res.ok, res.text
        return json.loads(res.text)
    else:
        print session.api + '/' + collection
        res = session.post(session.api + '/' + collection, data=data,
            allow_redirects=True)
        assert res.ok, res.text
        return json.loads(res.text)


def create_network(grano):
    #rest_upsert(session, 'networks', NETWORK, 'slug')
    net = grano.getNetwork()
    if net:
        grano.updateNetwork(NETWORK)
    else:
        grano.createNetwork(NETWORK)

    for type_, schema in (('entity', INTEREST),
                          ('relation', TURNOVER)):
        if grano.getSchema(type_, schema['name']):
            grano.updateSchema(type_, schema)
        else:
            grano.createSchema(type_, schema)



def create_reps(session, engine):
    for rep in sl.find(engine, sl.get_table(engine, 'representative')):
        rep['type'] = 'interest'
        rep['members'] = int(float(rep['members']))
        rep['title'] = rep['originalName']
        rep = convert_types(rep)
        rep_ent = entity_upsert(session, NETWORK['slug'] + '/entities', rep, 'identificationCode')
        for fdto in sl.find(engine, sl.get_table(engine, 'financialDataTurnover'), representativeEtlId=rep['etlId']):
            client = {
                'title': fdto['name'],
                'etlId': rep['etlId'],
                'etlFingerPrint': fdto['etlFingerPrint'],
                'type': 'interest'
                }
            client_ent = entity_upsert(session, NETWORK['slug'] + '/entities', client, 'title')
            rel = {
                'source': rep_ent['id'],
                'target': client_ent['id'],
                'source_id': rep_ent['id'],
                'target_id': client_ent['id'],
                'min': int(float(fdto['min'] or 0)),
                'max': int(float(fdto['max'] or 0)),
                'type': RELATION_TURNOVER_SCHEMA['name']
                }
            client_ent = entity_upsert(session, NETWORK['slug'] + '/relations', rel, 'source_id', 'target_id')


if __name__ == '__main__':
    engine = sl.connect(SETTINGS.ETL_URL)

    grano = GranoClient(SETTINGS.GRANO_API,
        network=NETWORK['slug'],
        api_user=SETTINGS.GRANO_AUTH[0],
        api_password=SETTINGS.GRANO_AUTH[1])
    create_network(grano)
    #create_reps(session, engine)
