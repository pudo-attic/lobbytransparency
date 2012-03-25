import logging
import sqlaload as sl

import SETTINGS
from schema import *
from queries import *
from setup import make_grano

log = logging.getLogger('load')

PROPS = {}


def canonical_actor(grano, engine, title):
    entity_table = sl.get_table(engine, 'entity')
    res = sl.find_one(engine, entity_table, etlFingerPrint=title)
    if res is not None and \
        'canonicalName' in res and \
        res['canonicalName'] and \
        title != res['canonicalName']:
        nonCanon = grano.findEntity(ACTOR['name'], title=title)
        if nonCanon:
            grano.deleteEntity(nonCanon)
        title = res['canonicalName']
    act = grano.findEntity(ACTOR['name'], title=title) or {}
    print [title]
    act['title'] = title
    act['type'] = ACTOR['name']
    return act


def replace_relation(lst, attribute, rel, match=['type']):
    new_list = [rel]
    cmp_ = [rel.get(attribute, {}).get('title')] + [rel.get(m) for m in match]
    for r in list(lst):
        if cmp_ == [r[attribute]['title']] + [r.get(m) for m in match]:
            continue
        new_list.append(r)
    return new_list


def find_relation(lst, attribute, other, props):
    p = props.items()
    cmp_ = [other.get('title')] + [v for k, v in p]
    for rel in lst:
        if cmp_ == [rel.get(attribute, {}).get('title')] + \
            [rel.get(k) for k, v in p]:
            return rel
    return props


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
        psn = canonical_actor(grano, engine, person['etlFingerPrint'])
        psn['firstName'] = person['firstName']
        psn['lastName'] = person['lastName']
        psn['salutation'] = person['title']
        psn['accreditationEndDate'] = person.get('accreditationEndDate')
        psn['accreditationStartDate'] = person.get('accreditationStartDate')
        psn['actsAsPerson'] = True

        rel = find_relation(rep['outgoing'], 'target', psn,
            {'type': EMPLOYMENT['name'], 'role': person['role']})
        rel['source'] = rep.get('id')
        rel['target'] = psn
        rel['position'] = person['position']
        rep['outgoing'] = replace_relation(rep['outgoing'], 'target', rel,
            match=['type', 'role'])
    return rep


def load_organisations(grano, engine, rep):
    for org in sl.find(engine, sl.get_table(engine, 'organisation'),
        representativeEtlId=rep['etlId']):
        ent = canonical_actor(grano, engine, org['name'])
        ent['members'] = int(float(org['numberOfMembers'] or 0))
        ent['actsAsOrganisation'] = True

        rel = find_relation(rep['outgoing'], 'target', ent,
            {'type': MEMBERSHIP['name']})
        rel['type'] = MEMBERSHIP['name']
        rel['source'] = rep.get('id')
        rel['target'] = ent
        rep['outgoing'] = replace_relation(rep['outgoing'], 'target', rel)
    return rep


def load_clients(grano, engine, rep):
    for fdto in sl.find(engine, sl.get_table(engine, 'financialDataTurnover'),
        representativeEtlId=rep['etlId']):
        del fdto['id']
        client = canonical_actor(grano, engine, fdto['name'])
        client.update(fdto)
        client['actsAsClient'] = True

        rel = find_relation(rep['incoming'], 'source', client,
            {'type': TURNOVER['name']})
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

        rel = find_relation(rep['outgoing'], 'target', int_,
            {'type': TOPIC['name']})
        rel['type'] = TOPIC['name']
        rel['source'] = rep.get('id')
        rel['target'] = int_
        rep['outgoing'] = replace_relation(rep['outgoing'], 'target', rel)
    return rep


def load_interests(grano, engine, rep):
    return load_proptable(grano, engine, rep, 'interest', INTEREST)


def load_action_fields(grano, engine, rep):
    return load_proptable(grano, engine, rep, 'actionField', ACTION_FIELD)


def load(engine, grano):
    for rep in sl.find(engine, sl.get_table(engine, 'representative')):
        del rep['id']
        rep_ent = canonical_actor(grano, engine, rep['originalName'])
        if 'id' in rep_ent:
            rep_ent = grano.getEntity(rep_ent['id'], deep=True)
        #if not SETTINGS.FULL and rep_ent['etlId'] == rep['etlId']:
        #    continue
        rep_ent.update(rep)
        rep_ent['actsAsRepresentative'] = True
        rep_ent['members'] = int(float(rep['members']))
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
        #raise ValueError()


if __name__ == '__main__':
    engine = sl.connect(SETTINGS.ETL_URL)
    grano = make_grano()
    load(engine, grano)