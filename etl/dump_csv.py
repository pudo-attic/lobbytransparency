from pprint import pprint

import sqlaload as sl


company_types = """SELECT "legalStatus", "contactCountry", COUNT(*) AS numHits FROM representative GROUP BY
                   "legalStatus", "contactCountry" ORDER BY "legalStatus" ASC;"""
entities = """SELECT * FROM entity;"""

def dump_query(engine, q, file_name):
    fh = open(file_name, 'wb')
    rp = engine.execute(q)
    sl.dump_csv(sl.resultiter(rp), fh)

if __name__ == '__main__':
    import sys
    assert len(sys.argv)==2, "Usage: %s [engine-url]"
    engine = sl.connect(sys.argv[1])
    #dump_query(engine, company_types, "legalStatus.csv")
    dump_query(engine, entities, "entity.csv")

