
QUERIES = [
    {
        'name': 'test',
        'label': 'Test Query',
        'query': 'SELECT * FROM entity_actor'
    },
    {
        'name': 'companies_by_exp',
        'label': 'TOP N companies (C II: companies and groups) spending most on lobbying',
        'query': 'SELECT id, title, "contactCountry", "fdCostAbsolute" as expenditure FROM entity_actor WHERE "subCategoryId" = 21 ORDER BY "fdCostAbsolute" DESC NULLS LAST'
    },
    {
        'name': 'rep_by_country',
        'label': 'Representatitives by country',
        'query': 'SELECT "contactCountry", COUNT(*) as number FROM entity_actor WHERE "actsAsRepresentative" = true GROUP BY "contactCountry" ORDER BY number DESC NULLS LAST'
    }

]
