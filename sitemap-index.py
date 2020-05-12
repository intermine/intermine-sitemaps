#!/usr/bin/env python

prefix = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
prefix += "<sitemapindex xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n" 

f = open("sitemap-index.xml","w")

f.write(prefix)

index = 0;

for index in range(0,2):
    f.write("<sitemap>\n")
    f.write("<loc>http://www.flymine.org/sitemap" + str(index) + ".xml</loc>\n")
    f.write("<lastmod>2019-07-31</lastmod>\n")
    f.write("<changefreq>monthly</changefreq><priority>0.5</priority>\n")
    f.write("</sitemap>\n")
    index += 1

f.write("</sitemapindex>\n")
f.close() 
