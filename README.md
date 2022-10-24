#  NewspaperSorter
This repo contains a set of tools for sorting a database of newspaper articles by the state they were published in.

The WebScrapers folder contains 3 python scripts which scrape data from different online databases which organize newspapers by their state of publication.
These scripts use the Request, and BeautifulSoup4 python packages. The directory structure is important so dont change it. Each script can be run at the command line as follows:

python3 \<scraper name\>

No command line args required.

The StateNewspaperFiles folder contains a script to combine all the papers from the scraper directories. The script can be run from the command line as:

python3 combinedScript.py





