from bs4 import BeautifulSoup
import lxml
import requests
import pandas as pd

def get_asee_urls(asee_url):
    website_url = requests.get(asee_url).text
    soup = BeautifulSoup(website_url, 'lxml')

    university_table = soup.find('table',{'class':'text'})
    university_links = university_table.findAll('a')
    universities = []
    links = []
    for link in university_links:
        universities.append(link.string)
        links.append(link.get('href'))

    dataframe = pd.DataFrame()
    dataframe['University'] = universities
    dataframe['Page Link'] = [("http://profiles.asee.org" + l) for l in links]
    dataframe['Undergraduate'] = ""
    dataframe['Graduate'] = ""
    dataframe['Engineering Technology'] = ""

    for i in range(0, len(dataframe)):
        current_school = dataframe.iloc[i]['Page Link']
        current_url = requests.get(current_school).text
        minisoup = BeautifulSoup(current_url, 'lxml').find('ul', {'id': 'sidenavlist'})
        heads = [s.text for s in minisoup.find_all('span')]
        lists = [s.find_all('a') for s in minisoup.find_all('ul')]

        link_titles = []
        for l in lists:
            link_titles.append([a.text for a in l])

        link_urls = []
        for l in lists:
            link_urls.append([("http://profiles.asee.org" + a.get('href')) for a in l])

        for x in range(0, len(heads)):
            if 'Enrollments by Class' in link_titles[x]:
                ind = link_titles[x].index('Enrollments by Class')
                dataframe.loc[i, heads[x]] = link_urls[x][ind]

    return dataframe
