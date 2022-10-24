#  NewspaperSorter
This repo contains a set of tools for sorting a database of newspaper articles (already sorted by year and month) by the state they were published in.

The input data should be .csv files of the following columns:

dateStamp, url, article length, title, article

the data needs to be stored in the following directory

\<year\> \ \<Month\> \ \<filename\>.csv

(note the months must have their first letter capitalized)

The directory structure in this repo is important and should not be changed.

The **WebScrapers** folder contains 3 python scripts which scrape data from different online databases which organize newspapers by their state of publication. The 4th file in the directory 
*ScraperUtil.py* contains data and file paths to be used by the scripts. These scripts use the Request, and BeautifulSoup4 python packages. The directory structure is important so dont change it. Each script can be run at the command line as follows:

`python3 \<scraper name\>`

No command line args required.

The **StateNewspaperFiles** folder contains a script to combine all the papers from the scraper directories. The script can be run from the command line as:

`python3 combinedScript.py`

The **ArticleSorter** folder contains 5 python scripts and a bash script.

*ArticleSorter.py* is the main python script which actually sorts the newspapers. It uses functions defined in *Util.py* and *RawDataHandler.py* to accomplish this. The syntax for calling the sorter from the command line is:

`python3 ArticleSorter \<year\>,\<month\> \<input_dir\> \<output_dir\> \<newspaper_dir\>`

where,

-- \<year\>,\<month\> 
-- \<input_dir\>
-- \<output_dir\>
-- \<newspaper_dir\>





