import logging
import csv, os

from recon import company
import sqlaload as sl

from common import integrate_recon
from normalize import normalize_text

import SETTINGS

log = logging.getLogger('load')

def update_entities(engine, file_name):
    log.info("Updateing entities reference sheet: %s", file_name)
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
        if not row.get('canonicalName'):
            row['canonicalName'] = row['etlFingerPrint']
        entity = data.get(fp)
        if entity and entity.get('canonicalName') and \
            fp != entity.get('canonicalName'):
            print entity.get('canonicalName').encode('utf-8')
            row['canonicalName'] = entity.get('canonicalName')
            out = row.copy()
            del out['id']
            sl.upsert(engine, table, out, ['etlFingerPrint'])
        if writer is None:
            writer = csv.DictWriter(fh, row.keys())
            writer.writerow(dict(zip(row.keys(), row.keys())))
        r = [(k, unicode(v).encode('utf-8')) for k, v in row.items()]
        writer.writerow(dict(r))
    fh.close()


def create_entities(engine):
    log.info("De-normalizing global entities collection...")
    table = sl.get_table(engine, 'entity')
    for tbl in ['representative', 'person', 'financialDataTurnover',
        'organisation']:
        for row in sl.all(engine, sl.get_table(engine, tbl)):
            entity = {'etlFingerPrint': row.get('etlFingerPrint')}
            entity['legalStatus'] = row.get('legalStatus', '')
            entity['countryCode'] = row.get('contactCountryCode', '')
            entity['etlTable'] = tbl
            sl.upsert(engine, table, entity, ['etlFingerPrint', 'etlTable'])


def recon_companies(engine):
    integrate_recon(engine, sl.get_table(engine, 'entity'),
                    company, 'etlFingerPrint',
                    'canonicalName', 'canonicalURI')


def cluster(engine):
    for row in sl.all(engine, sl.get_table(engine, 'entity')):
        print normalize_text(row['etlFingerPrint']).encode('utf-8')


if __name__ == '__main__':
    engine = sl.connect(SETTINGS.ETL_URL)
    create_entities(engine)
    update_entities(engine, 'entities.csv')
    #recon_companies(engine)
    #cluster(engine)
