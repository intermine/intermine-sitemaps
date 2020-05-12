#!/usr/bin/env python

# This script requires the InterMine python client.
#
# For further documentation you can visit:
#     http://intermine.readthedocs.org/en/latest/web-services/

# to run this script, run python sitemap.py "organism name" "intermine-url"

from intermine.webservice import Service
import sys

print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))

mineUrl = sys.argv[1]
serviceUrl = mineUrl + "/service"
organism = None

if (len(sys.argv) > 2):
    organism = sys.argv[2]

print("Generating sitemap for organism: ", organism, ", serviceUrl: ", serviceUrl)

service = Service(serviceUrl)

# Get a new query on the class (table) you will be querying:
query = service.new_query("Gene")

# The view specifies the output columns
query.add_view("primaryIdentifier")

query.add_constraint("primaryIdentifier", "IS NOT NULL", code = "A")

if (organism):
    query.add_constraint("organism.name", "=", organism, code = "B")

# Uncomment and edit the code below to specify your own custom logic:
# query.set_logic("A")

sitemapCount = 0;

prefix = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
prefix = prefix + "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\"\n"
prefix = prefix + "  xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n"
prefix = prefix + "  xsi:schemaLocation=\"http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd\">\n"

postfix = "</urlset>"

rowCount = 0

f = open('sitemap' + str(sitemapCount) + ".xml",'w')

f.write(prefix)

for row in query.rows():
    urlStr = "<url><loc>" + mineUrl + "/portal.do?externalids=" + row["primaryIdentifier"].strip() + "</loc></url>\n";
    f.write(urlStr)
    rowCount = rowCount + 1
    if rowCount >= 50000:
        f.write(postfix)
        f.close()
        sitemapCount = sitemapCount + 1
        f = open('sitemap' + str(sitemapCount) + ".xml",'w')
        f.write(prefix)
        rowCount = 1
f.write(postfix)
f.close()
