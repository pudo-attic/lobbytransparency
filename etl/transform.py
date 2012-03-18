import logging
import sqlaload as sl

import SETTINGS
from schema import *

log = logging.getLogger('transform')

CATEGORIES = {
    u'I - Professional consultancies/law firms/self-employed consultants': 1,
    u'II - In-house lobbyists and trade/professional associations': 2,
    u'III - Non-governmental organisations': 3,
    u'IV - Think tanks, research and academic institutions': 4,
    u'V - Organisations representing churches and religious communities': 5,
    u'VI - Organisations representing local, regional and municipal authorities, other public or mixed entities, etc.': 6
    }

SUBCATEGORIES = {
    u'Law firms': 11,
    u'Professional consultancies': 12,
    u'Self-employed consultants': 13,
    u'Companies & groups': 21,
    u'Other similar organisations': 22,
    u'Trade unions': 23,
    u'Trade, business & professional associations': 24,
    u'Non-governmental organisations, platforms and networks and similar': 31,
    u'Academic institutions': 41,
    u'Think tanks and research institutions': 42,
    u'Organisations representing churches and religious communities': 51,
    u'Local, regional and municipal authorities (at sub-national level)': 61,
    u'Other public or mixed entities, etc.': 62
    }

def code_categories(engine):
    table = sl.get_table(engine, 'representative')
    for cat in sl.distinct(engine, table, 'mainCategory'):
        cat['mainCategoryId'] = CATEGORIES[cat['mainCategory']]
        sl.upsert(engine, table, cat, ['mainCategory'])

def code_subcategories(engine):
    table = sl.get_table(engine, 'representative')
    for cat in sl.distinct(engine, table, 'subCategory'):
        cat['subCategoryId'] = SUBCATEGORIES[cat['subCategory']]
        sl.upsert(engine, table, cat, ['subCategory'])

def transform(engine):
    log.info("Performing micro-transforms...")
    code_categories(engine)
    code_subcategories(engine)

if __name__ == '__main__':
    engine = sl.connect(SETTINGS.ETL_URL)
    transform(engine)
