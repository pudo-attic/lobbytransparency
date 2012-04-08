import logging
import csv
import os

import sqlaload as sl

from normalize import normalize_text, reverse_normalize

import SETTINGS

log = logging.getLogger('load')


def update_entities(engine, file_name):
    log.info("Updating entities reference sheet: %s", file_name)
    data = {}
    if os.path.exists(file_name):
        fh = open(file_name, 'rb')
        reader = csv.DictReader(fh)
        data = {}
        for d in reader:
            e = [(k, v.decode('utf-8')) for (k, v) in d.items()]
            e = dict(e)
            data[e['etlFingerPrint']] = e
        fh.close()
        print len(data)

    fh = open(file_name, 'wb')
    writer = None
    table = sl.get_table(engine, 'entity')
    for row in sl.all(engine, table):
        fp = row['etlFingerPrint']
        if fp is None:
            continue
        if not row.get('canonicalName'):
            row['canonicalName'] = row['etlFingerPrint']
        row['canonicalName'] = cleanCanonical(row['canonicalName'])
        entity = data.get(fp)
        if entity and entity.get('canonicalName') and \
            fp != entity.get('canonicalName'):
            #print entity.get('canonicalName').encode('utf-8')
            row['canonicalName'] = entity.get('canonicalName')
            out = row.copy()
            del out['id']
            sl.upsert(engine, table, out, ['etlFingerPrint'])
        cn = row['canonicalName']
        row['normalizedForm'] = normalize_text(cn)
        row['reverseForm'] = reverse_normalize(cn)
        if writer is None:
            writer = csv.DictWriter(fh, row.keys())
            writer.writerow(dict(zip(row.keys(), row.keys())))
        r = [(k, unicode(v).encode('utf-8')) for k, v in row.items()]
        writer.writerow(dict(r))
    fh.close()


def cleanCanonical(name):
    name = name.strip()
    name = name.replace('\t', ' ')
    name = name.replace('\n', ' ')
    name = name.replace('\r', ' ')
    name = name.replace('  ', ' ')
    name = name.replace('  ', ' ')
    name = name.replace('  ', ' ')
    return name


def create_entities(engine):
    log.info("De-normalizing global entities collection...")
    table = sl.get_table(engine, 'entity')
    for tbl in ['representative', 'person', 'financialDataTurnover',
        'organisation', 'network_entity']:
        for row in sl.all(engine, sl.get_table(engine, tbl)):
            entity = {'etlFingerPrint': row.get('etlFingerPrint')}
            entity['legalStatus'] = row.get('legalStatus', '')
            entity['countryCode'] = row.get('contactCountryCode', '')
            entity['etlTable'] = tbl
            sl.upsert(engine, table, entity, ['etlFingerPrint', 'etlTable'])


def cluster(engine):
    for row in sl.all(engine, sl.get_table(engine, 'entity')):
        print normalize_text(row['etlFingerPrint']).encode('utf-8')


if __name__ == '__main__':
    engine = sl.connect(SETTINGS.ETL_URL)
    create_entities(engine)
    update_entities(engine, 'entities.csv')
    #cluster(engine)
