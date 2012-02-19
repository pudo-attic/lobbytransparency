#!/bin/bash
#
# Download XML dumps. Hardcoded paths (yuk!)

curl -o /var/www/opendatalabs.org/eu/lobbyists/data-old-`date +"%Y-%m-%d"`.xml "http://ec.europa.eu/transparencyregister/public/consultation/statistics.do?action=getLobbyistsXml&fileType=OLD"
curl -o /var/www/opendatalabs.org/eu/lobbyists/data-new-`date +"%Y-%m-%d"`.xml "http://ec.europa.eu/transparencyregister/public/consultation/statistics.do?action=getLobbyistsXml&fileType=NEW"
