#!/usr/bin/env python

# This script requires the InterMine python client.
#
# For further documentation you can visit:
#     http://intermine.readthedocs.org/en/latest/web-services/

# to run this script, run python sitemap.py "intermine-url" "organism name" "frequency-of-update".
# organism name is optional, as is frequency of update
# examples:
#    python sitemap.py "https://test.intermine.org/covidmine"
#    python sitemap.py "https://test.intermine.org/covidmine" "Homo sapiens"
#    python sitemap.py "https://test.intermine.org/covidmine" "Homo sapiens" "monthly"
#    python sitemap.py "https://test.intermine.org/covidmine" "" "daily"

from intermine.webservice import Service
from datetime import date
import sys

def generateMapEntry( identifier, mineUrl ):
    """Generates a single URL XML entry for an entity"""
    urlStr = "<url><loc>" + mineUrl + "/portal.do?externalids=" + identifier.strip() + "</loc></url>\n";
    return urlStr

def writeMapEntriesToFile( theQuery, columnToWrite, mineUrl, theFile, rowCount):
    """Output results for only one query and write to file."""
    for row in theQuery.rows():
        theFile.write(generateMapEntry(row[columnToWrite], mineUrl))
        rowCount = rowCount + 1
        if rowCount >= 50000:
            theFile.write(postfix)
            theFile.close()
            sitemapCount = sitemapCount + 1
            theFile = open('sitemap' + str(sitemapCount) + ".xml",'w')
            theFile.write(prefix)
            rowCount = 1

# take arguments from the command line and generate map for proteins and genes.
mineUrl = sys.argv[1]
serviceUrl = mineUrl + "/service"
organism = None
updateFrequency = "monthly"

if (len(sys.argv) > 2):
    organism = sys.argv[2]

if (len(sys.argv) > 3):
    updateFrequency = sys.argv[3]

print("Generating sitemap for organism: ", organism, ", serviceUrl: ", serviceUrl, "update frequency", updateFrequency)

service = Service(serviceUrl)

# Query Gene
geneQuery = service.new_query("Gene")
geneQuery.add_view("primaryIdentifier")
geneQuery.add_constraint("primaryIdentifier", "IS NOT NULL", code = "A")

# Query Protein
proteinQuery = service.new_query("Protein")
proteinQuery.add_view("primaryAccession")
proteinQuery.add_constraint("primaryAccession", "IS NOT NULL", code = "A")

# Query Genome
genomeQuery = service.new_query("Genome")
genomeQuery.add_view("primaryIdentifier")
genomeQuery.add_constraint("primaryIdentifier", "IS NOT NULL", code = "A")

# only restrain by organism if we're supposed to...
if (organism):
    geneQuery.add_constraint("organism.name", "=", organism, code = "B")
    proteinQuery.add_constraint("organism.name", "=", organism, code = "B")

prefix = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
prefix = prefix + "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\"\n"
prefix = prefix + "  xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n"
prefix = prefix + "  xsi:schemaLocation=\"http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd\">\n"

postfix = "</urlset>"

sitemapCount = 0;
rowCount = 0



#Write sitemap to a file
f = open('sitemap' + str(sitemapCount) + ".xml",'w')

f.write(prefix)

writeMapEntriesToFile(proteinQuery, "primaryAccession", mineUrl, f, rowCount)
writeMapEntriesToFile(geneQuery, "primaryIdentifier", mineUrl, f, rowCount)
writeMapEntriesToFile(genomeQuery, "primaryIdentifier", mineUrl, f, rowCount)

f.write(postfix)
f.close()

## Write sitemap index - we may have multiple sitemaps if there are a lot of
## entities in Gene and protein
prefix = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
prefix += "<sitemapindex xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n"

f = open("sitemap-index.xml","w")

f.write(prefix)

index = 0;

# format today's date for the last update
today = date.today()
updateDate = today.strftime("%Y-%m-%d")

# print out the location of the sitemap(s)
for index in range(0,(sitemapCount+1)):
    f.write("<sitemap>\n")
    f.write("<loc>" + mineUrl + "/sitemap" + str(index) + ".xml</loc>\n")
    f.write("<lastmod>" + updateDate + "</lastmod>\n")
    f.write("<changefreq>" + updateFrequency + "</changefreq><priority>0.5</priority>\n")
    f.write("</sitemap>\n")
    index += 1

f.write("</sitemapindex>\n")
f.close()
