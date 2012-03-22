import logging
import sqlaload as sl

from granoclient import GranoClient

import SETTINGS
from schema import *

log = logging.getLogger('load')

PROPS = {}


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


def replace_relation(list, attribute, rel, match=['type']):
    new_list = []
    found = False
    for r in list:
        checks = [r.get(m) == rel.get(m) for m in match]
        if (r[attribute].get('id') == rel[attribute].get('id') or \
            r[attribute].get('title') == rel[attribute].get('title')) \
            and not False in checks:
            found = True
            new_list.append(rel)
        else:
            new_list.append(r)
    if not found:
        new_list.append(rel)
    return new_list


def find_relation(rep, type, source=None, target=None):
    key = lambda e: e.get('id') if isinstance(e, dict) else e
    if source is not None:
        for rel in rep['incoming']:
            if rel['type'] != type:
                continue
            if key(rel['source']) == source:
                return rel
    if target is not None:
        for rel in rep['outgoing']:
            if rel['type'] != type:
                continue
            if key(rel['target']) == target:
                return rel
    return {}


def get_financial_data(engine, rep):
    fds = list(sl.find(engine, sl.get_table(engine, 'financialData'),
        representativeEtlId=rep['etlId']))
    fd = max(fds, key=lambda f: f.get('endDate'))
    for key, value in fd.items():
        if key in [u'totalBudget', u'turnoverMin', u'costAbsolute', u'publicFinancingNational',
            u'otherSourcesDonation', u'eurSourcesProcurement', u'costMax', u'eurSourcesGrants',
            u'otherSourcesContributions', u'publicFinancingTotal', u'turnoverAbsolute',
            u'turnoverMax', u'costMin', u'directRepCostsMin', u'directRepCostsMax',
            u'publicFinancingInfranational', u'otherSourcesTotal']:
            if value is not None:
                value = int(float(value))
        key = 'fd' + key[0].upper() + key[1:]
        rep[key] = value
    return rep


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
        psn['accreditationEndDate'] = person.get('accreditationEndDate')
        psn['accreditationStartDate'] = person.get('accreditationStartDate')
        psn['actsAsPerson'] = True

        rel = find_relation(rep, EMPLOYMENT['name'], target=psn.get('id'))
        rel['type'] = EMPLOYMENT['name']
        rel['source'] = rep.get('id')
        rel['target'] = psn
        rel['role'] = person['role']
        rel['position'] = person['position']
        rep['outgoing'] = replace_relation(rep['outgoing'], 'target', rel,
            match=['type', 'role'])
    return rep


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

        rel = find_relation(rep, MEMBERSHIP['name'], target=ent.get('id'))
        rel['type'] = MEMBERSHIP['name']
        rel['source'] = rep.get('id')
        rel['target'] = ent
        rep['outgoing'] = replace_relation(rep['outgoing'], 'target', rel)
    return rep


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

        rel = find_relation(rep, TURNOVER['name'], source=client.get('id'))
        rel['type'] = TURNOVER['name']
        rel['source'] = client
        rel['target'] = rep.get('id')
        rel['min'] = int(float(fdto['min'] or 0))
        rel['max'] = int(float(fdto['max'] or 0))
        rep['incoming'] = replace_relation(rep['incoming'], 'source', rel)
    return rep


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

        rel = find_relation(rep, TOPIC['name'], source=int_.get('id'))
        rel['type'] = TOPIC['name']
        rel['source'] = rep.get('id')
        rel['target'] = int_
        rep['outgoing'] = replace_relation(rep['outgoing'], 'target', rel)
    return rep


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
        if 'id' in rep_ent:
            rep_ent = grano.getEntity(rep_ent['id'], deep=True)
        #if not SETTINGS.FULL and rep_ent['etlId'] == rep['etlId']:
        #    continue
        rep_ent.update(rep)
        rep_ent['type'] = ACTOR['name']
        rep_ent['actsAsRepresentative'] = True
        rep_ent['members'] = int(float(rep['members']))
        rep_ent['title'] = title
        rep_ent['incoming'] = rep_ent.get('incoming', [])
        rep_ent['outgoing'] = rep_ent.get('outgoing', [])
        rep_ent = load_clients(grano, engine, rep_ent)
        rep_ent = load_organisations(grano, engine, rep_ent)
        rep_ent = load_persons(grano, engine, rep_ent)
        rep_ent = load_interests(grano, engine, rep_ent)
        rep_ent = load_action_fields(grano, engine, rep_ent)
        rep_ent = get_financial_data(engine, rep_ent)
        # TODO: other financial sources
        #from pprint import pprint
        #pprint(rep_ent)
        grano.updateEntity(rep_ent)


def load(engine):
    log.info("Beginning to load data into Grano: %s", SETTINGS.GRANO_API)
    grano = GranoClient(SETTINGS.GRANO_API,
        network=NETWORK['slug'],
        api_user=SETTINGS.GRANO_AUTH[0],
        api_password=SETTINGS.GRANO_AUTH[1])
    create_network(grano)
    load_representatives(grano, engine)

if __name__ == '__main__':
    engine = sl.connect(SETTINGS.ETL_URL)
    load(engine)