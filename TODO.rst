Microtasks
==========

* Assign codes to organization groups. 
* 






* ETL Model:
  * ``representative``
  * ``person``
  * ``interest``
  * ``financial_data``
  * ``member_organisations``


Cleaning tasks
--------------



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
* Countries (to ISO2)

What information can be used for de-duplication? 

* Source table (e.g. all legal/head are natural persons)
* ``legalStatus`` and suffix in company name

What is the goal? An entity table of the form: 

* ``etlFingerPrint`` -Source surface form
* ``etlTable`` - table in which it occurred (representative, person, org)
* ``canonicalName`` - final and unique name
* ``canonicalType`` - a type within a custom taxonomy (tbd)
* ``canonicalURI`` - a URI (e.g. OpenCorporates) associated with the entity.
  Use home pages when given (and no reconciliation was feasible)?


Munging performed
-----------------

* There are two types of customer turnover statements for legal
  representation: absolute ranges and percentage ranges. Since for
  percentage ranges we have the total lobbying expenditure, we're
  munging the percentage figures into absolute figures very early
  in ETL. (cf.: customersGroupsInAbsoluteRange,
  customersGroupsInPercentageRange)
* Customized sources of income are divided into "public" and "other"
  in the source schema. In the ETL version, this is a flag on the 
  same table.


