from urllib import urlopen 

from recon.local import CSVLocalEndpoint
import sqlaload as sl

from common import integrate_recon

COUNTRIES_URL = 'countrycodes.csv'

def integrate_countries(engine):
    fh = urlopen(COUNTRIES_URL)
    uri = lambda r: r['ISO-2']
    endpoint = CSVLocalEndpoint(fh, 'Country', uri_maker=uri)
    integrate_recon(engine, sl.get_table(engine, 'representative'), 
                    endpoint.reconcile,
                    'contactCountry',
                    'contactCountryName', 'contactCountryCode',
                    memory_name='recon_countryNames')
    integrate_recon(engine, sl.get_table(engine, 'countryOfMember'), 
                    endpoint.reconcile,
                    'countryOfMember',
                    'countryOfMemberName', 'countryOfMemberCode',
                    memory_name='recon_countryNames')

if __name__ == '__main__':
    import sys
    assert len(sys.argv)==2, "Usage: %s [engine-url]"
    engine = sl.connect(sys.argv[1])
    integrate_countries(engine)


