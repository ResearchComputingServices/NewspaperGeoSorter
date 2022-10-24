import requests
from bs4 import BeautifulSoup


# COMMON DATA

stateNamesList = [  'Alabama', 'Alaska', 'Arkansas', 'American_Samoa', 'Arizona',
                'California', 'Colorado', 'Connecticut', 'Washington,_D.C.', 'Delaware',
                'Florida', 'Georgia_(U.S._state)', 'Guam', 'Hawaii', 'Iowa', 'Idaho', 'Illinois', 'Indiana',
                'Kansas', 'Kentucky', 'Louisiana', 'Massachusetts', 'Maryland', 'Maine', 'Michigan',
                'Minnesota', 'Missouri', 'Mississippi', 'Montana', 'North_Carolina', 'North_Dakota',
                'Nebraska', 'New_Hampshire', 'New_Jersey', 'New_Mexico', 'Nevada', 'New_York', 'Ohio',
                'Oklahoma', 'Oregon', 'Pennsylvania', 'Puerto_Rico', 'Rhode_Island', 'South_Carolina',
                'South_Dakota', 'Tennessee', 'Texas', 'Utah', 'Virginia', 'the_United_States_Virgin_Islands', 'Vermont',
                'Washington_(state)', 'Wisconsin', 'West_Virginia', 'Wyoming']

# Data for WikiScraper only
wikiBaseURL = 'https://en.wikipedia.org'
wikiResultsDirectory = './Wiki_Output'
baseStateNewsPapersURL = wikiBaseURL + '/wiki/List_of_newspapers_in_'

skipWords = ['University', 'College', 'Institute' ]
failedTerms = ['Dead Wiki Link', 'No URL Found', 'URL Not Found', 'No URL Found in infobox']

numberOfAttempts = 10

targetHeaders = [   'Dailies',
                    'Daily_newspapers',
                    'Daily_Newspapers',
                    'daily_newspapers',
                    'Non-Daily_newspapers',
                    'Nondaily_newspapers',
                    'Daily_newspapers_(currently_published)',
                    'Daily_newspapers_and_Online_Publications_(currently_published)',
                    'Weeklies'
                    'Weekly_newspapers',
                    'Weekly_newspapers',
                    'Weekly_and_other_newspapers',
                    'Weekly_newspapers_(currently_published)',
                    'Biweekly_newspapers',
                    'Biweekly_newspapers_(currently_published)',
                    'Monthly_newspapers',
                    'Monthly_newspapers_(currently_published)',
                    'University_newspapers',
                    'University_newspaper',
                    'Daily_and_nondaily_newspapers',
                    'Daily_and_nondaily_newspapers_(currently_published)',
                    'Daily_and_weekly_newspapers_(currently_published)',
                    'List_of_newspapers',
                    'Current_news_publications',
                    'Newspapers_of_record',
                    'Regional_papers',
                    'Regional_and_local',
                    'Daily,_weekly,_online_newspapers_(currently_published)',
                    'Major_daily_newspapers',
                    'Special_interest_newspapers',
                    'Community_papers',
                    'Daily_and_weekly_newspapers_(currently_published_in_Colorado)',
                    'Smaller_newspapers',
                    'Daily,_weekly,_and_other_newspapers',
                    'College_newspapers',
                    'Major_daily',
                    'Major_papers',
                    'Refional_and_local',
                    'College']

# Data for W3NewsScraper only
w3NewsBaseURL = 'https://www.w3newspapers.com/usa/'
w3NewsOutputDir = './W3News_Output/'

# Data for usnplScraper only

usnplBaseURL = 'https://www.usnpl.com/search/state?state='
usnplOutputDir = './USNPL_Output/'

stateNamesDict = {  'Alabama' : 'AL', 
                    'Alaska' : 'AK', 
                    'Arkansas' : 'AR', 
                    'American_Samoa' : 'AS', 
                    'Arizona' : 'AZ',
                    'California' : 'CA', 
                    'Colorado' : 'CO', 
                    'Connecticut' : 'CT', 
                    'Washington,_D.C.' : 'DC', 
                    'Delaware' : 'DE',
                    'Florida' : 'FL', 
                    'Georgia_(U.S._state)' : 'GA', 
                    'Guam' : 'GU', 
                    'Hawaii' : 'HI', 
                    'Iowa' : 'IA', 
                    'Idaho' : 'ID', 
                    'Illinois' : 'IL', 
                    'Indiana' : 'IN',
                    'Kansas' : 'KS', 
                    'Kentucky' : 'KY', 
                    'Louisiana' : 'LA', 
                    'Massachusetts' : 'MA', 
                    'Maryland' : 'MD', 
                    'Maine' : 'ME', 
                    'Michigan' : 'MI',
                    'Minnesota' : 'MN', 
                    'Missouri' : 'MO', 
                    'Mississippi' : 'MS', 
                    'Montana' : 'MT', 
                    'North_Carolina' : 'NC', 
                    'North_Dakota' : 'ND',
                    'Nebraska' : 'NE', 
                    'New_Hampshire' : 'NH', 
                    'New_Jersey' : 'NJ', 
                    'New_Mexico' : 'NM', 
                    'Nevada' : 'NV', 
                    'New_York' : 'NY', 
                    'Ohio' : 'OH',
                    'Oklahoma' : 'OK', 
                    'Oregon' : 'OR', 
                    'Pennsylvania' : 'PA', 
                    'Puerto_Rico' : 'PR', 
                    'Rhode_Island' : 'RI', 
                    'South_Carolina' : 'SC',
                    'South_Dakota' : 'SD', 
                    'Tennessee' : 'TN', 
                    'Texas' : 'TX', 
                    'Utah' : 'UT', 
                    'Virginia' : 'VA', 
                    'the_United_States_Virgin_Islands' : 'VI', 
                    'Vermont' : 'VT',
                    'Washington_(state)' : 'WA', 
                    'Wisconsin' : 'WI', 
                    'West_Virginia' : 'WV', 
                    'Wyoming': 'WY'}



# This function takes in a URL and returns a BeautifulSoup parsed object
def ParseWebpage(webpageURL):

    webPage = requests.get(webpageURL)
    webPageParsed = BeautifulSoup(webPage.content, 'html.parser')

    return webPageParsed