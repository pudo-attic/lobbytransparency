import SETTINGS
import logging

import sqlaload as sl

from extract import extract
from entities import create_entities, update_entities
from load import load


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    import sys
    assert len(sys.argv) == 2, "Usage: %s [source_file]"
    source_file = sys.argv[1]
    engine = sl.connect(SETTINGS.ETL_URL)
    extract(engine, source_file)
    create_entities(engine)
    update_entities(engine, 'entities.csv')
    load(engine)
