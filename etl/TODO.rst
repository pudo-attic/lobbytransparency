Extract/Transform/Load Microtasks
=================================

* ETL Model:
  * ``representative``
  * ``person``
  * ``interest``
  * ``financial_data``
  * ``member_organisations``

What is the final data model?
-----------------------------

* Do we want to produce a single entity table with natural persons and 
  organizations of various types combined in it?
* How do we store historic data - do we flag current revisions with a 
  special flag?
* Where does manual editing (e.g. classification) happen: ETL or 
  production? 
* How do we handle obviously bad entities (e.g. someone pasting a link to
  a database, instead of a members list?)

Deduplication
-------------

* Use custom deduplication code or Center of Responsive Politics code?

* Company types (in representatives)
* Persons (unexpected, large overlap)



Munging performed
-----------------

* There are two types of customer turnover statements for legal
  representation: absolute ranges and percentage ranges. Since for
  percentage ranges we have the total lobbying expenditure, we're
  munging the percentage figures into absolute figures very early
  in ETL. (cf.: customersGroupsInAbsoluteRange,
  customersGroupsInPercentageRange)



