
QUERIES = [
    {
        'name': 'test',
        'label': 'Test Query',
        'query': 'SELECT * FROM entity_actor'
        },
    {
        'name': 's1',
        'label': 'TOP N companies (C II: companies and groups) spending most on lobbying',
        'query': 'SELECT id, title, "contactCountry", "fdCostAbsolute" as expenditure FROM entity_actor WHERE "subCategoryId" = 21 ORDER BY "fdCostAbsolute" DESC'
    }
]
