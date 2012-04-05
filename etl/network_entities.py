import logging
import csv
import os

import sqlaload as sl

from normalize import normalize_text, reverse_normalize

import SETTINGS

log = logging.getLogger('load')


def update_network_entities(engine, file_name):
    log.info("Updating network entities reference sheet: %s", file_name)
    network_entities = set()
    table = sl.get_table(engine, 'network_entity')
    if os.path.exists(file_name):
        fh = open(file_name, 'rb')
        reader = csv.DictReader(fh)
        for d in reader:
            e = [(k, v.decode('utf-8')) for (k, v) in d.items()]
            e = dict(e)
            network_entities.add((e['identificationCode'], e['etlFingerPrint']))
            sl.upsert(engine, table, e, ['identificationCode', 'etlFingerPrint'])
        fh.close()
        reps = set([ne[0] for ne in network_entities])
        rep_table = sl.get_table(engine, 'representative')
        for rep in reps:
            sl.update(engine, rep_table, {'identificationCode': rep}, {'network_extracted': True})

    for row in sl.all(engine, table):
        network_entities.add((row['identificationCode'], row['etlFingerPrint']))

    fh = open(file_name, 'wb')
    writer = None
    table = sl.get_table(engine, 'network_entity')
    for ic, fp in network_entities:
        row = {
            'identificationCode': ic,
            'etlFingerPrint': fp
        }
        if writer is None:
            writer = csv.DictWriter(fh, row.keys())
            writer.writerow(dict(zip(row.keys(), row.keys())))
        r = [(k, unicode(v).encode('utf-8')) for k, v in row.items()]
        writer.writerow(dict(r))
    fh.close()



if __name__ == '__main__':
    engine = sl.connect(SETTINGS.ETL_URL)
    update_network_entities(engine, 'network_entities.csv')
    #cluster(engine)
