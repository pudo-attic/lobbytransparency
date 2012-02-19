from pprint import pprint

import sqlaload as sl
import load_xml

def load_person(person, role, childBase, engine):
    table = sl.get_table(engine, 'person')
    person_ = childBase.copy()
    person_.update(person)
    person_['role'] = role
    person_['etlFingerPrint'] = '%s %s %s' % (person['title'] or '',
                                              person['firstName'],
                                              person['lastName'])
    person_['etlFingerPrint'] = person_['etlFingerPrint'].strip()
    sl.upsert(engine, table, person_, ['representativeEtlId',
                                       'etlFingerPrint'])

def load_finances(financialData, childBase, engine):
    etlId = '%s//%s' % (financialData['startDate'].isoformat(),
                        financialData['endDate'].isoformat())

    financial_sources = \
        [(s, 'other') for s in financialData.pop("otherCustomized")] + \
        [(s, 'public') for s in financialData.pop("publicCustomized")]
    for financial_source, type_ in financial_sources:
        financial_source['type'] = type_
        financial_source['financialDataEtlId'] = etlId
        financial_source.update(childBase)
        sl.upsert(engine, sl.get_table(engine, 'financialDataCustomSource'),
                  financial_source, ['representativeEtlId',
                      'financialDataEtlId', 'type', 'name'])

    for turnover in financialData.pop("turnoverBreakdown"):
        turnover['financialDataEtlId'] = etlId
        turnover['etlFingerPrint'] = turnover['name'].strip()
        turnover.update(childBase)
        sl.upsert(engine, sl.get_table(engine, 'financialDataTurnover'),
                  turnover, ['representativeEtlId', 'financialDataEtlId', 
                             'etlFingerPrint'])

    financialData['etlId'] = etlId
    financialData.update(childBase)
    sl.upsert(engine, sl.get_table(engine, 'financialData'),
              financialData, ['representativeEtlId', 'etlId'])
    #pprint(financialData)

def load_rep(rep, engine):
    etlId = rep['etlId'] = "%s//%s" % (rep['identificationCode'],
                                       rep['lastUpdateDate'].isoformat())
    childBase = {'representativeEtlId': etlId, 
                 'representativeUpdateDate': rep['lastUpdateDate']}
    load_person(rep.pop('legalPerson'), 'legal', childBase, engine)
    load_person(rep.pop('headPerson'), 'head', childBase, engine)
    for actionField in rep.pop('actionFields'):
        rec = childBase.copy()
        rec['actionField'] = actionField
        sl.upsert(engine, sl.get_table(engine, 'actionField'), rec,
                  ['representativeEtlId', 'actionField'])

    for interest in rep.pop('interests'):
        rec = childBase.copy()
        rec['interest'] = interest
        sl.upsert(engine, sl.get_table(engine, 'interest'), rec,
                  ['representativeEtlId', 'interest'])

    for countryOfMember in rep.pop('countryOfMembers'):
        rec = childBase.copy()
        rec['countryOfMember'] = countryOfMember
        sl.upsert(engine, sl.get_table(engine, 'countryOfMember'), rec,
                  ['representativeEtlId', 'countryOfMember'])

    for organisation in rep.pop('organisations'):
        rec = childBase.copy()
        rec.update(organisation)
        rec['etlFingerPrint'] = organisation['name'].strip()
        sl.upsert(engine, sl.get_table(engine, 'organisation'), rec,
                  ['representativeEtlId', 'etlFingerPrint'])

    load_finances(rep.pop('fd'), childBase, engine)
    #pprint(rep)
    rep['etlFingerPrint'] = rep['originalName'].strip()
    sl.upsert(engine, sl.get_table(engine, 'representative'), rep,
              ['etlId'])


def load_etldb(source_file, engine):
    for i, rep in enumerate(load_xml.parse(source_file)):
        load_rep(rep, engine)
        if i % 100 == 0:
            print i, "..."

if __name__ == '__main__':
    import sys
    assert len(sys.argv)==3, "Usage: %s [source_file] [engine-url]"
    source_file = sys.argv[1]
    engine = sl.connect(sys.argv[2])
    load_etldb(source_file, engine)






