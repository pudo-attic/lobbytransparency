
QUERIES = [
    {
        'name': 'test',
        'label': 'Test Query',
        'query': 'SELECT * FROM entity_actor'
    },
    {
        'name': 'actor_by_exp',
        'label': 'Actors spending most on lobbying in a subcategory',
        'query': 'SELECT id, title, "contactCountry", GREATEST("fdCostAbsolute", "fdCostMax") as expenditure FROM entity_actor WHERE "subCategoryId" = :subCategoryId ORDER BY expenditure DESC NULLS LAST'
    },
    {
        'name': 'rep_by_country',
        'label': 'Representatitives by country',
        'query': 'SELECT "contactCountry", COUNT(*) as number FROM entity_actor WHERE "actsAsRepresentative" = true GROUP BY "contactCountry" ORDER BY number DESC NULLS LAST'
    },
    {
        'name': 'actor_by_turnover',
        'label': 'Actors with the biggest lobbying turnover in a subcategory',
        'query': 'SELECT id, title, "contactCountry", "fdTurnoverMax" as turnover FROM entity_actor WHERE "subCategoryId" = :subCategoryId ORDER BY "fdTurnoverMax" DESC NULLS LAST'
    },
    {
        'name': 'actor_by_fte',
        'label': 'Actors with the most lobbyists employed in a subcategory',
        'query': 'SELECT ea.id AS id, ea.title AS title, ea."contactCountry" as "contactCountry", ea."staffMembers" AS members, COUNT(re.id) as accreditations FROM entity_actor ea LEFT JOIN relation_employment re ON re.source_id = ea.id WHERE ea."subCategoryId" = :subCategoryId AND re.role = \'accredited\' GROUP BY ea.id, ea.title, ea."staffMembers", ea."contactCountry" ORDER BY members DESC NULLS LAST'
    },
    {
        'name': 'fte_by_subcategory',
        'label': 'Categories of actors with the most lobbyists employed',
        'query': 'SELECT ea."subCategory" AS "subCategory", COUNT(ea."staffMembers") AS members, (SELECT COUNT(re.id) FROM relation_employment re LEFT JOIN entity_actor e ON re.source_id = e.id WHERE e."subCategory" = ea."subCategory" AND re.role = \'accredited\') as accreditations FROM entity_actor ea WHERE ea."actsAsRepresentative" = true GROUP BY ea."subCategory" ORDER BY members DESC NULLS LAST'
    }

]
