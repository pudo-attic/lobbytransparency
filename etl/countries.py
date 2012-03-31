import sqlaload as sl
import csv

import SETTINGS

COUNTRIES_URL = 'countrycodes.csv'


def read_reference():
    fh = open(COUNTRIES_URL, 'rb')
    reader = csv.DictReader(fh)
    data = []
    for row in reader:
        data.append(row)
    fh.close()
    return data


def write_reference(data):
    fh = open(COUNTRIES_URL, 'wb')
    columns = set()
    for row in data:
        columns.update(row.keys())
    writer = csv.DictWriter(fh, columns)
    writer.writerow(dict(zip(columns, columns)))
    for row in data:
        writer.writerow(row)
    fh.close()


def update_reference(engine, data, table_name, col):
    table = sl.get_table(engine, table_name)
    for row in sl.distinct(engine, table, col):
        print row
        matched = False
        for ref in data:
            country = ref['country'].decode('utf-8')
            if ref['euname'] == row[col] or \
                country.upper() == row[col].upper():
                if not len(ref['euname']):
                    ref['euname'] = row[col]
                matched = True
                sl.update_row(engine, table, {
                        col: row[col],
                        col + 'Norm': country,
                        col + 'Code': ref['iso2']},
                        [col])
        if not matched:
            print row
    return data


def transform_countries(engine):
    data = read_reference()
    data = update_reference(engine, data, 'representative', 'contactCountry')
    data = update_reference(engine, data, 'countryOfMember', 'countryOfMember')
    write_reference(data)

if __name__ == '__main__':
    engine = sl.connect(SETTINGS.ETL_URL)
    #integrate_countries(engine)
    transform_countries(engine)
