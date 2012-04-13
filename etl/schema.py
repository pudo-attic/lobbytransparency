
NETWORK = {
    'slug': 'eutr',
    'title': 'European Parliament and Commission Transparency Register'
    }


TURNOVER = {
    'label': 'Lobbying turnover',
    'name': 'turnover',
    'attributes': {
        'min': {
            'type': 'integer',
            'label': 'Minimum',
            'help': ''
            },
        'max': {
            'type': 'integer',
            'label': 'Maximum',
            'help': ''
            }
        }
    }

EMPLOYMENT = {
    'label': 'Employment',
    'name': 'employment',
    'attributes': {
        'role': {
            'type': 'string',
            'label': 'Role',
            'help': ''
            },
        'position': {
            'type': 'string',
            'label': 'Position',
            'help': ''
            }
        }
    }

MEMBERSHIP = {
    'label': 'Membership',
    'name': 'member',
    'attributes': {}
    }

ASSOCIATED = {
    'label': 'Associated',
    'name': 'associated',
    'attributes': {}
    }

TOPIC = {
    'label': 'Topic',
    'name': 'topic',
    'attributes': {}
    }

INTEREST = {
    'label': 'Interest',
    'name': 'interest',
    'attributes': {}
    }

ACTION_FIELD = {
    'label': 'Action Field',
    'name': 'action_field',
    'attributes': {}
    }

ACTOR = {
    'label': 'Registered Interest',
    'name': 'actor',
    'attributes': {
        'actsAsRepresentative': {
            'type': 'boolean',
            'label': 'Actor is a representative',
            'missing': '0',
            'help': ''
            },
        'actsAsClient': {
            'type': 'boolean',
            'label': 'Actor is a client',
            'missing': '0',
            'help': ''
            },
        'actsAsPerson': {
            'type': 'boolean',
            'label': 'Actor is a natual person',
            'missing': '0',
            'help': ''
            },
        'actsAsOrganisation': {
            'type': 'boolean',
            'label': 'Actor is an organisation',
            'missing': '0',
            'help': ''
            },

        'firstName': {
            'type': 'string',
            'label': 'First Name',
            'help': ''
            },
        'lastName': {
            'type': 'string',
            'label': 'Last Name',
            'help': ''
            },
        'salutation': {
            'type': 'string',
            'label': 'Salutation',
            'help': ''
            },
        'accreditationStartDate': {
            'type': 'date',
            'label': 'EP Accreditation Start Date',
            'help': ''
            },
        'accreditationEndDate': {
            'type': 'date',
            'label': 'EP Accreditation End Date',
            'help': ''
            },

        'acronym': {
            'type': 'string',
            'label': 'Acronym',
            'help': ''
            },
        'activities': {
            'type': 'string',
            'label': 'Activities',
            'help': ''
            },
        'codeOfConduct': {
            'type': 'string',
            'label': 'Code of Conduct',
            'help': ''
            },
        'contactCountry': {
            'type': 'string',
            'label': 'Country',
            'help': ''
            },
        'contactFax': {
            'type': 'string',
            'label': 'Fax Nr.',
            'help': ''
            },
        'contactIndicFax': {
            'type': 'string',
            'label': 'Indic Fax Nr.',
            'help': ''
            },
        'contactIndicPhone': {
            'type': 'string',
            'label': 'Indic Phone Nr.',
            'help': ''
            },
        'contactMore': {
            'type': 'string',
            'label': 'More details',
            'help': ''
            },
        'contactNumber': {
            'type': 'string',
            'label': 'Nr.',
            'help': ''
            },
        'contactPhone': {
            'type': 'string',
            'label': 'Tel. Nr.',
            'help': ''
            },
        'contactPostCode': {
            'type': 'string',
            'label': 'Post Code',
            'help': ''
            },
        'contactStreet': {
            'type': 'string',
            'label': 'Street',
            'help': ''
            },
        'contactTown': {
            'type': 'string',
            'label': 'Town',
            'help': ''
            },
        'etlId': {
            'type': 'string',
            'label': 'ETL-ID',
            'help': ''
            },
        'identificationCode': {
            'type': 'string',
            'label': 'Identification code',
            'help': ''
            },
        'lastUpdateDate': {
            'type': 'date',
            'label': 'Last Update',
            'help': ''
            },
        'legalStatus': {
            'type': 'string',
            'label': 'Legal Status',
            'help': ''
            },
        'mainCategory': {
            'type': 'string',
            'label': 'Category',
            'help': ''
            },
        'mainCategoryId': {
            'type': 'integer',
            'label': 'Category (ID)',
            'help': ''
            },
        'staffMembers': {
            'type': 'integer',
            'label': 'Staff Members',
            'help': ''
            },
        'orgMembers': {
            'type': 'integer',
            'label': 'Organisation Members',
            'help': ''
            },
        'networking': {
            'type': 'string',
            'label': 'Networking Activities',
            'help': ''
            },
        'numberOfNaturalPersons': {
            'type': 'integer',
            'label': 'Number of natural persons',
            'help': ''
            },
        'numberOfOrganisations': {
            'type': 'integer',
            'label': 'Number of organisations',
            'help': ''
            },
        'registrationDate': {
            'type': 'date',
            'label': 'Date of registration',
            'help': ''
            },
        'status': {
            'type': 'string',
            'label': 'Status',
            'help': ''
            },
        'subCategory': {
            'type': 'string',
            'label': 'Sub-Category',
            'help': ''
            },
        'subCategoryId': {
            'type': 'integer',
            'label': 'Sub-Category ID',
            'help': ''
            },
        'webSiteURL': {
            'type': 'string',
            'label': 'Web site URL',
            'help': ''
            },


        'fdDirectRepCostsMax': {
            'type': 'integer',
            'label': 'Direct representation costs (max)',
            'help': ''
            },
        'fdType': {
            'type': 'string',
            'label': 'Financial reporting type',
            'help': ''
            },
        'fdPublicFinancingTotal': {
            'type': 'integer',
            'label': 'Public financing (total)',
            'help': ''
            },
        'fdOtherSourcesDonation': {
            'type': 'integer',
            'label': 'Other sources: Donations',
            'help': ''
            },
        'fdTurnoverAbsolute': {
            'type': 'integer',
            'label': 'Turnover (absolute)',
            'help': ''
            },
        'fdOtherSourcesTotal': {
            'type': 'integer',
            'label': 'Other sources (total)',
            'help': ''
            },
        'fdEurSourcesGrants': {
            'type': 'integer',
            'label': 'European financing (grants)',
            'help': ''
            },
        'fdCostMax': {
            'type': 'integer',
            'label': 'Cost (max)',
            'help': ''
            },
        'fdPublicFinancingNational': {
            'type': 'integer',
            'label': 'Public financing (national)',
            'help': ''
            },
        'fdDirectRepCostsMin': {
            'type': 'integer',
            'label': 'Direct representation costs (min)',
            'help': ''
            },
        'fdTotalBudget': {
            'type': 'integer',
            'label': 'Total budget',
            'help': ''
            },
        'fdStartDate': {
            'type': 'date',
            'label': 'Financial reporting start date',
            'help': ''
            },
        'fdTurnoverMax': {
            'type': 'integer',
            'label': 'Turnover (max)',
            'help': ''
            },
        'fdEurSourcesProcurement': {
            'type': 'integer',
            'label': 'European financing (procurement)',
            'help': ''
            },
        'fdPublicFinancingInfranational': {
            'type': 'integer',
            'label': 'Public financing (infranational)',
            'help': ''
            },
        'fdCostMin': {
            'type': 'integer',
            'label': 'Cost (min)',
            'help': ''
            },
        'fdEndDate': {
            'type': 'date',
            'label': 'Financial reporting end date',
            'help': ''
            },
        'fdTurnoverMin': {
            'type': 'integer',
            'label': 'Turnover (max)',
            'help': ''
            },
        'fdCostAbsolute': {
            'type': 'integer',
            'label': 'Cost (absolute)',
            'help': ''
            },
        'fdOtherSourcesContributions': {
            'type': 'integer',
            'label': 'Other sources (contributions)',
            'help': ''
            }
        }
    }
