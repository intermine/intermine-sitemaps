# intermine-sitemaps
generates a sitemap for your (jsp-based) intermine.

## Running the script

### Dependencies

- Python 3+
- the [InterMine python client](https://github.com/intermine/intermine-ws-python#downloading)

### generating a sitemap

To run this script, run python sitemap.py "intermine-url" "organism name" "update-frequency".
Organism name and frequency are optional, URL is required. Don't add `/service` to the end!


#### examples

```bash
#    python sitemap.py "https://test.intermine.org/covidmine"
#    python sitemap.py "https://test.intermine.org/covidmine" "Homo sapiens"
#    python sitemap.py "https://test.intermine.org/covidmine" "Homo sapiens" "monthly"
#    python sitemap.py "https://test.intermine.org/covidmine" "" "daily"
```
