#  NewspaperSorter
This repo contains a set of tools for sorting a database of newspaper articles (already sorted by year and month) by the state they were published in.

The input data should be .csv files of the following columns:

`dateStamp, url, article length, title, article`

the data needs to be stored in the following directory:

`~\<year>\<Month>\<filename>.csv`

(note the months must have their first letter capitalized)

The directory structure in this repo is important and should not be changed.


The file output is stored

## Web Scrapers 
The **WebScrapers** folder contains 3 python scripts which scrape data from different online databases which organize newspapers by their state of publication. The 4th file in the directory 
*ScraperUtil.py* contains data and file paths to be used by the scripts. These scripts use the Request, and BeautifulSoup4 python packages. The directory structure is important so dont change it. Each script can be run at the command line as follows:

`python3 <scraper name>.py`

No command line args required. The output from these scrapers are CSV files for each state containing the papers name and it's base URL. For example the first few entries in **Alabama.csv** are:

`Sand Mountain Reporter,http://www.sandmountainreporter.com/` <br>
`Alexander City Outlook,http://www.alexcityoutlook.com/` <br>
`Andalusia Star-News,http://www.andalusiastarnews.com/` <br>

## State Newspaper directory

The **StateNewspaperFiles** folder contains a script to combine all the papers from the scraper directories. The script can be run from the command line as:

`python3 combinedScript.py`

## ArticleSorter

The **ArticleSorter** folder contains 5 python scripts and a bash script. The *ResultsAnalyzer.py* and *StateNewspaperAnalyzer.py* scripts are not required for the sorting and will be ignored. For the curious, they can be used to get diagonistic data on the newspaper database as well as the results of the sorting. 

*ArticleSorter.py* is the main python script which actually sorts the newspapers. It uses functions defined in *Util.py* and *RawDataHandler.py* to accomplish this. The syntax for calling the sorter from the command line is:

`python3 ArticleSorter <year>,<month> <input_dir> <output_dir> <newspaper_dir>`

where,

* `<year>,<month>`   the year and month of the input data ex. 2016,March
* `<input_dir>`        the file path to the base of the input data directory tree
* `<output_dir>`       the file path to the base where to save the data too
* `<newspaper_dir>`    the file path to the base of where the state sorted newspaper files are (ie. the output of *combinedScript.py*)


the output of the *ArticleSorter.py* is a directory tree organized as follows:

`<output_dir>\States\<state name>\<year>\<Month>\<state name>_<year>_<Month>.csv`

for example:

`<output_dir> States/Alabama/2016/September/Alabama_2016_September.csv`

there is also a directory called **Reports** which contains information on the number of articles found, the number skipped, and other diagonistics for each state/month/year.







