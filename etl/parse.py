from datetime import datetime
from lxml import etree
from pprint import pprint

#import model

SRC = 'http://ec.europa.eu/transparencyregister/public/consultation/statistics.do?action=getLobbyistsXml&fileType=NEW'
_NS2 = "http://www.w3.org/1999/xlink"
#_NS="http://intragate.ec.europa.eu/transparencyregister/intws/20090623_new"
_NS = "http://intragate.ec.europa.eu/transparencyregister/intws/20110715"
_SI = "http://www.w3.org/2001/XMLSchema-instance"
NS = '{%s}' % _NS
NS2 = '{%s}' % _NS2
SI = '{%s}' % _SI

_AP = "http://ec.europa.eu/transparencyregister/accreditedPerson/V1"
AP = '{%s}' % _AP


def dateconv(ds):
    return datetime.strptime(ds.split("+")[0], "%Y-%m-%dT%H:%M:%S.%f")


def ap_dateconv(ds):
    return datetime.strptime(ds, "%Y-%m-%d+%H:%M")


def parse_rep(rep_el):
    rep = {}
    rep['identificationCode'] = rep_el.findtext(NS + 'identificationCode')
    rep['status'] = rep_el.findtext(NS + 'status')
    rep['registrationDate'] = dateconv(rep_el.findtext(NS + 'registrationDate'))
    rep['lastUpdateDate'] = dateconv(rep_el.findtext(NS + 'lastUpdateDate'))
    rep['legalStatus'] = rep_el.findtext(NS + 'legalStatus')
    rep['acronym'] = rep_el.findtext(NS + 'acronym')
    rep['originalName'] = rep_el.findtext('.//' + NS + 'originalName')
    el = rep_el.find(NS + 'webSiteURL')
    rep['webSiteURL'] = el.get(NS2 + 'href') if el is not None else None
    rep['mainCategory'] = rep_el.findtext('.//' + NS + 'mainCategory')
    rep['subCategory'] = rep_el.findtext('.//' + NS + 'subCategory')

    legal = {}
    legal['title'] = rep_el.findtext(NS + 'legal/' + NS + 'title')
    legal['firstName'] = rep_el.findtext(NS + 'legal/' + NS +
            'firstName')
    legal['lastName'] = rep_el.findtext(NS + 'legal/' + NS +
            'lastName')
    legal['position'] = rep_el.findtext(NS + 'legal/' + NS +
            'position')
    rep['legalPerson'] = legal

    head = {}
    head['title'] = rep_el.findtext(NS + 'head/' + NS + 'title')
    head['firstName'] = rep_el.findtext(NS + 'head/' + NS +
            'firstName')
    head['lastName'] = rep_el.findtext(NS + 'head/' + NS +
            'lastName')
    head['position'] = rep_el.findtext(NS + 'head/' + NS +
            'position')
    rep['headPerson'] = head

    rep['contactStreet'] = rep_el.findtext(NS + 'contactDetails/' + NS + 'street')
    rep['contactNumber'] = rep_el.findtext(NS + 'contactDetails/' + NS + 'number')
    rep['contactPostCode'] = rep_el.findtext(NS + 'contactDetails/' + NS
            + 'postCode')
    rep['contactTown'] = rep_el.findtext(NS + 'contactDetails/' + NS
            + 'town')
    rep['contactCountry'] = rep_el.findtext(NS + 'contactDetails/' + NS
            + 'country')
    rep['contactIndicPhone'] = rep_el.findtext(NS + 'contactDetails//' + NS
            + 'indicPhone')
    rep['contactIndicFax'] = rep_el.findtext(NS + 'contactDetails//' + NS
            + 'indicFax')
    rep['contactFax'] = rep_el.findtext(NS + 'contactDetails//' + NS
            + 'fax')
    rep['contactPhone'] = rep_el.findtext(NS + 'contactDetails//' + NS
            + 'phoneNumber')
    rep['contactMore'] = rep_el.findtext(NS + 'contactDetails/' + NS
            + 'moreContactDetails')
    rep['goals'] = rep_el.findtext(NS + 'goals')
    rep['networking'] = rep_el.findtext(NS + 'networking')
    rep['activities'] = rep_el.findtext(NS + 'activities')
    rep['codeOfConduct'] = rep_el.findtext(NS + 'codeOfConduct')
    rep['members'] = rep_el.findtext(NS + 'members')
    rep['actionFields'] = []
    for field in rep_el.findall('.//' + NS + 'actionField/' + NS +
            'actionField'):
        rep['actionFields'].append(field.text)
    rep['interests'] = []
    for interest in rep_el.findall('.//' + NS + 'interest/' + NS +
            'name'):
        rep['interests'].append(interest.text)
    rep['numberOfNaturalPersons'] = rep_el.findtext(NS + 'structure/' + NS
            + 'numberOfNaturalPersons')
    rep['numberOfOrganisations'] = rep_el.findtext(NS + 'structure/' + NS
            + 'numberOfOrganisations')
    rep['countryOfMembers'] = []
    el = rep_el.find(NS + 'structure/' + NS + 'countries')
    if el is not None:
        for country in el.findall('.//' + NS + 'country'):
            rep['countryOfMembers'].append(country.text)
    rep['organisations'] = []
    el = rep_el.find(NS + 'structure/' + NS + 'organisations')
    if el is not None:
        for org_el in el.findall(NS + 'organisation'):
            org = {}
            org['name'] = org_el.findtext(NS + 'name')
            org['numberOfMembers'] = org_el.findtext(NS + 'numberOfMembers')
            rep['organisations'].append(org)

    fd_el = rep_el.find(NS + 'financialData')
    fd = {}
    fd['startDate'] = dateconv(fd_el.findtext(NS + 'startDate'))
    fd['endDate'] = dateconv(fd_el.findtext(NS + 'endDate'))
    fd['eurSourcesProcurement'] = fd_el.findtext(NS + 'eurSourcesProcurement')
    fd['eurSourcesGrants'] = fd_el.findtext(NS + 'eurSourcesGrants')
    fi = fd_el.find(NS + 'financialInformation')
    fd['type'] = fi.get(SI + 'type')
    #import ipdb; ipdb.set_trace()
    fd['totalBudget'] = fi.findtext('.//' + NS +
        'totalBudget')
    fd['publicFinancingTotal'] = fi.findtext('.//' + NS +
        'totalPublicFinancing')
    fd['publicFinancingNational'] = fi.findtext('.//' + NS +
        'nationalSources')
    fd['publicFinancingInfranational'] = fi.findtext('.//' + NS +
        'infranationalSources')
    cps = fi.find('.//' + NS + 'customisedPublicSources')
    fd['publicCustomized'] = []
    if cps is not None:
        for src_el in cps.findall(NS + 'customizedSource'):
            src = {}
            src['name'] = src_el.findtext(NS + 'name')
            src['amount'] = src_el.findtext(NS + 'amount')
            fd['publicCustomized'].append(src)
    fd['otherSourcesTotal'] = fi.findtext('.//' + NS +
        'totalOtherSources')
    fd['otherSourcesDonation'] = fi.findtext('.//' + NS +
        'donation')
    fd['otherSourcesContributions'] = fi.findtext('.//' + NS +
        'contributions')
    # TODO customisedOther
    cps = fi.find('.//' + NS + 'customisedOther')
    fd['otherCustomized'] = []
    if cps is not None:
        for src_el in cps.findall(NS + 'customizedSource'):
            src = {}
            src['name'] = src_el.findtext(NS + 'name')
            src['amount'] = src_el.findtext(NS + 'amount')
            fd['otherCustomized'].append(src)

    fd['directRepCostsMin'] = fi.findtext('.//' + NS +
        'directRepresentationCosts//' + NS + 'min')
    fd['directRepCostsMax'] = fi.findtext('.//' + NS +
        'directRepresentationCosts//' + NS + 'max')
    fd['costMin'] = fi.findtext('.//' + NS +
        'cost//' + NS + 'min')
    fd['costMax'] = fi.findtext('.//' + NS +
        'cost//' + NS + 'max')
    fd['costAbsolute'] = fi.findtext('.//' + NS +
        'cost//' + NS + 'absoluteAmount')
    fd['turnoverMin'] = fi.findtext('.//' + NS +
        'turnover//' + NS + 'min')
    fd['turnoverMax'] = fi.findtext('.//' + NS +
        'turnover//' + NS + 'max')
    fd['turnoverAbsolute'] = fi.findtext('.//' + NS +
        'turnover//' + NS + 'absoluteAmount')
    tb = fi.find(NS + 'turnoverBreakdown')
    fd['turnoverBreakdown'] = []
    if tb is not None:
        for range_ in tb.findall(NS + 'customersGroupsInAbsoluteRange'):
            max_ = range_.findtext('.//' + NS + 'max')
            min_ = range_.findtext('.//' + NS + 'min')
            for customer in range_.findall('.//' + NS + 'customer'):
                fd['turnoverBreakdown'].append({
                    'name': customer.findtext(NS + 'name'),
                    'min': min_,
                    'max': max_
                    })
        for range_ in tb.findall(NS + 'customersGroupsInPercentageRange'):
            # FIXME: I hate political compromises going into DB design
            # so directly.
            max_ = range_.findtext('.//' + NS + 'max')
            if max_:
                max_ = float(max_) / 100.0 * \
                        float(fd['turnoverAbsolute'] or
                                fd['turnoverMax'] or fd['turnoverMin'])
            min_ = range_.findtext('.//' + NS + 'min')
            if min_:
                min_ = float(min_) / 100.0 * \
                        float(fd['turnoverAbsolute'] or
                                fd['turnoverMin'] or fd['turnoverMax'])
            for customer in range_.findall('.//' + NS + 'customer'):
                fd['turnoverBreakdown'].append({
                    'name': customer.findtext(NS + 'name'),
                    'min': min_,
                    'max': max_
                    })
    rep['fd'] = fd
    return rep


def parse(file_name):
    doc = etree.parse(file_name)
    for rep_el in doc.findall('//' + NS + 'interestRepresentativeNew'):
        rep = parse_rep(rep_el)
        #pprint(rep)
        yield rep


def parse_ap(file_name):
    doc = etree.parse(file_name)
    for ap_el in doc.findall('//' + AP + 'accreditedPerson'):
        ap = {
            'orgIdentificationCode': ap_el.findtext(AP + 'orgIdentificationCode'),
            'numberOfIR': ap_el.findtext(AP + 'numberOfIR'),
            'orgName': ap_el.findtext(AP + 'orgName'),
            'title': ap_el.findtext(AP + 'title'),
            'firstName': ap_el.findtext(AP + 'firstName'),
            'lastName': ap_el.findtext(AP + 'lastName'),
            'accreditationStartDate': ap_dateconv(ap_el.findtext(AP + 'accreditationStartDate')),
            'accreditationEndDate': ap_dateconv(ap_el.findtext(AP + 'accreditationEndDate')),
            }
        yield ap
