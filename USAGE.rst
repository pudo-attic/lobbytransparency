How to use the LobbyTransparency codebase
=========================================

As with all data-cleansing/aggregation efforts, this project will likely
generate a collection of scripts that need to be run in a particular 
environment, order and configuration. I'll try to keep track of this as
cleanly as possible, but otherwise ask: friedrich@pudo.org

It is important to realize that the LobbyTransparency site depends on 
another piece of software, ``grano``, to provide backend storage for 
the resulting lobby graph. For more information on grano, check out:

  http://github.com/pudo/grano


Creating the virtualenv
-----------------------

All python scripts should be run within a virtualenv (Python runtime 
sandbox) so that their dependencies do not pollute the global namespace.
On most systems, virtualenv can be installed easily::

  $ sudo apt-get install python-virtualenv
  # or:
  $ sudo easy_install virtualenv

Once the software is installed, creating the environment (e.g. inside
the working directory of this project) is simple::

  $ git clone https://github.com/okfn/lobbytransparency
  $ cd lobbytransparency
  $ virtualenv pyenv

  # Repeat this step whenever you want to enter the environment in a 
  # fresh terminal:
  $ source pyenv/bin/activate
  # Install dependencies (e.g. flask, lxml):
  $ pip install -r pip-requirements.txt


Extracting content from the XML dumps
-------------------------------------

In order to guarantee historic availability of the XML dumps, we're 
archiving both versions of the file ("OLD" and "NEW") each day through an
ETL server at http://opendatalabs.org/eu/lobbyists. The first task
therefore is to download this archive::

  $ cd etl
  $ ./fetch_archive.sh

Alternatively, there is a simple script to execute the whole ETL process
with remote data::

  $ cd etl
  $ sh update.sh

This requires that you adapt the settings in ``SETTINGS.py`` to match your
local environment (ETL postgres database URI, grano instance).



