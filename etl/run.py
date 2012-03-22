import SETTINGS
import logging

import sqlaload as sl

from extract import extract
from entities import create_entities, update_entities
from load import load
from transform import transform


if __name__ == '__main__':
    import sys
    logging.basicConfig(level=logging.DEBUG)
    assert len(sys.argv) == 3, "Usage: %s [ir_source_file] [ap_source_file]"
    ir_source_file = sys.argv[1]
    ap_source_file = sys.argv[2]
    engine = sl.connect(SETTINGS.ETL_URL)
    extract(engine, ir_source_file, ap_source_file)
    create_entities(engine)
    update_entities(engine, 'entities.csv')
    transform(engine)
    load(engine)