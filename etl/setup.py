import logging
import sqlaload as sl

from granoclient import GranoClient

import SETTINGS
from schema import *
from queries import *

log = logging.getLogger('setup')


def make_grano():
    grano = GranoClient(SETTINGS.GRANO_API,
        network=NETWORK['slug'],
        api_user=SETTINGS.GRANO_AUTH[0],
        api_password=SETTINGS.GRANO_AUTH[1])
    return grano


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

    for query in QUERIES:
        if grano.getQuery(query['name']):
            grano.updateQuery(query)
        else:
            grano.createQuery(query)


def setup(engine, grano):
    log.info("Configuring Grano: %s", SETTINGS.GRANO_API)
    create_network(grano)

if __name__ == '__main__':
    engine = sl.connect(SETTINGS.ETL_URL)
    grano = make_grano()
    setup(engine, grano)