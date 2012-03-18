
Question 1:

SELECT title FROM entity_actor WHERE "subCategoryId" = 21 ORDER BY "fdDirectfdCostsMax" DESC LIMIT 10;

Random choice: fdDirectfdCostsMax 

SELECT title, COUNT("members") as num_lobbyists FROM entity_actor WHERE "subCategoryId" = 21 GROUP BY title ORDER BY num_lobbyists DESC LIMIT 10;



SELECT ea.title, COUNT(re.id) AS num_ep FROM entity_actor ea LEFT JOIN relation_employment re ON re.source_id = ea.id WHERE ea."mainCategoryId" = 2 AND re.role = 'accredited' GROUP BY ea.title ORDER BY num_ep DESC LIMIT 10;

