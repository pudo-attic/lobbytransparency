import SETTINGS
import logging

import sqlaload as sl

from extract import extract
from entities import create_entities, update_entities
from load import load
from setup import setup, make_grano
from transform import transform
from network_entities import update_network_entities


if __name__ == '__main__':
    import sys
    logging.basicConfig(level=logging.DEBUG)
    assert len(sys.argv) == 3, "Usage: %s [ir_source_file] [ap_source_file]"
    ir_source_file = sys.argv[1]
    ap_source_file = sys.argv[2]
    engine = sl.connect(SETTINGS.ETL_URL)
    extract(engine, ir_source_file, ap_source_file)
    create_entities(engine)
    update_network_entities(engine, 'network_entities.csv')
    update_entities(engine, 'entities.csv')
    transform(engine)
    grano = make_grano()
    setup(engine, grano)
    load(engine, grano)
