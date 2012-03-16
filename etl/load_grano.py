import sqlaload as sl

from granoclient import GranoClient

import SETTINGS
from schema import *


def create_network(grano):
    net = grano.getNetwork()
    if net:
        grano.updateNetwork(NETWORK)
    else:
        grano.createNetwork(NETWORK)

    for type_, schema in (('entity', ACTOR),
                          ('entity', ACTION_FIELD),
                          ('entity', INTEREST),
                          ('relation', TURNOVER),
                          ('relation', MEMBERSHIP),
                          ('relation', TOPIC),
                          ('relation', EMPLOYMENT)):
        if grano.getSchema(type_, schema['name']):
            grano.updateSchema(type_, schema)
        else:
            grano.createSchema(type_, schema)


def canonical_name(grano, engine, title, type=ACTOR['name']):
    entity_table = sl.get_table(engine, 'entity')
    res = sl.find_one(engine, entity_table, etlFingerPrint=title)
    if res is None or not 'canonicalName' in res or \
        res['canonicalName'] is None or title == res['canonicalName']:
        return title
    nonCanon = grano.findEntity(type, title=title)
    if nonCanon:
        grano.deleteEntity(nonCanon)
    return res['canonicalName']


def get_financial_data(engine, rep):
    fds = list(sl.find(engine, sl.get_table(engine, 'financialData'),
        representativeEtlId=rep['etlId']))
    fd = max(fds, key=lambda f: f.get('endDate'))
    fo = {}
    for key, value in fd.items():
        if key in [u'totalBudget', u'turnoverMin', u'costAbsolute', u'publicFinancingNational',
            u'otherSourcesDonation', u'eurSourcesProcurement', u'costMax', u'eurSourcesGrants',
            u'otherSourcesContributions', u'publicFinancingTotal', u'turnoverAbsolute',
            u'turnoverMax', u'costMin', u'directfdCostsMin', u'directfdCostsMax',
            u'publicFinancingInfranational', u'otherSourcesTotal']:
            if value is not None:
                value = int(float(value))
        key = 'fd' + key[0].upper() + key[1:]
        fo[key] = value
    return fo


def load_persons(grano, engine, rep):
    for person in sl.find(engine, sl.get_table(engine, 'person'),
        representativeEtlId=rep['etlId']):
        del person['id']
        title = canonical_name(grano, engine, person['etlFingerPrint'])
        psn = grano.findEntity(ACTOR['name'], title=title) or {}
        psn['type'] = ACTOR['name']
        psn['title'] = title
        psn['firstName'] = person['firstName']
        psn['lastName'] = person['lastName']
        psn['salutation'] = person['title']
        psn['actsAsPerson'] = True
        psn = grano.updateEntity(psn)

        rel = grano.findRelation(EMPLOYMENT['name'],
                source_id=rep['id'],
                target_id=psn['id']) or {}
        rel['type'] = EMPLOYMENT['name']
        rel['source'] = rep
        rel['target'] = psn
        rel['role'] = person['role']
        rel = grano.updateRelation(rel)


def load_organisations(grano, engine, rep):
    for org in sl.find(engine, sl.get_table(engine, 'organisation'),
        representativeEtlId=rep['etlId']):
        del org['id']
        title = canonical_name(grano, engine, org['name'])
        ent = grano.findEntity(ACTOR['name'], title=title) or {}
        ent['type'] = ACTOR['name']
        ent['title'] = title
        ent['members'] = int(float(org['numberOfMembers'] or 0))
        ent['actsAsOrganisation'] = True
        ent = grano.updateEntity(ent)

        rel = grano.findRelation(MEMBERSHIP['name'],
                source_id=rep['id'],
                target_id=ent['id']) or {}
        rel['type'] = MEMBERSHIP['name']
        rel['source'] = rep
        rel['target'] = ent
        rel = grano.updateRelation(rel)


def load_clients(grano, engine, rep):
    for fdto in sl.find(engine, sl.get_table(engine, 'financialDataTurnover'),
        representativeEtlId=rep['etlId']):
        del fdto['id']
        title = canonical_name(grano, engine, fdto['name'])
        client = grano.findEntity(ACTOR['name'], title=title) or {}
        client.update(fdto)
        client['type'] = ACTOR['name']
        client['title'] = title
        client['actsAsClient'] = True
        client = grano.updateEntity(client)

        rel = grano.findRelation(TURNOVER['name'],
                source_id=client['id'],
                target_id=rep['id']) or {}
        rel['type'] = TURNOVER['name']
        rel['source'] = client
        rel['target'] = rep
        rel['min'] = int(float(fdto['min'] or 0))
        rel['max'] = int(float(fdto['max'] or 0))
        rel = grano.updateRelation(rel)

PROPS = {}
def load_proptable(grano, engine, rep, prop, schema):
    for row in sl.find(engine, sl.get_table(engine, prop),
        representativeEtlId=rep['etlId']):
        if (prop, row[prop]) in PROPS:
            int_ = PROPS[(prop, row[prop])]
        else:
            del row['id']
            int_ = grano.findEntity(schema['name'], title=row[prop]) or {}
            if int_.get('title') != row[prop]:
                int_['type'] = schema['name']
                int_['title'] = row[prop]
                int_ = grano.updateEntity(int_)
            PROPS[(prop, row[prop])] = int_

        rel = grano.findRelation(TOPIC['name'],
                source_id=rep['id'],
                target_id=int_['id']) or {}
        if not rel.get('id'):
            rel['type'] = TOPIC['name']
            rel['source'] = rep
            rel['target'] = int_
            grano.updateRelation(rel)


def load_interests(grano, engine, rep):
    return load_proptable(grano, engine, rep, 'interest', INTEREST)


def load_action_fields(grano, engine, rep):
    return load_proptable(grano, engine, rep, 'actionField', ACTION_FIELD)


def load_representatives(grano, engine):
    for rep in sl.find(engine, sl.get_table(engine, 'representative')):
        del rep['id']
        # TODO: name resolution
        title = canonical_name(grano, engine, rep['originalName'])
        rep_ent = grano.findEntity(ACTOR['name'], title=title) or {}
        rep_ent.update(rep)
        rep_ent['type'] = ACTOR['name']
        rep_ent['actsAsRepresentative'] = True
        rep_ent['members'] = int(float(rep['members']))
        rep_ent['title'] = title
        # TODO: other financial sources
        rep_ent.update(get_financial_data(engine, rep_ent))
        rep_ = grano.updateEntity(rep_ent)
        load_clients(grano, engine, rep_)
        load_organisations(grano, engine, rep_)
        load_persons(grano, engine, rep_)
        load_interests(grano, engine, rep_)
        load_action_fields(grano, engine, rep_)


if __name__ == '__main__':
    engine = sl.connect(SETTINGS.ETL_URL)

    grano = GranoClient(SETTINGS.GRANO_API,
        network=NETWORK['slug'],
        api_user=SETTINGS.GRANO_AUTH[0],
        api_password=SETTINGS.GRANO_AUTH[1])
    create_network(grano)
    load_representatives(grano, engine)
