import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
from aseescraper import *

# return a dataframe containing the rows from the undergrad level of each school
def scrape_undergrad(school, undergrad_url, data_columns):
    years = ['Freshmen', 'Sophomore', 'Junior', 'Senior']
    df = pd.DataFrame(columns=data_columns)
    try:
        tables = pd.read_html(undergrad_url, header=0)
    except:
        return df

    if len(tables) != 5:
        print("hmm... " + school)
        return df

    # interate through index table and create rows w/ Total
    for x in range(0, len(tables[0])):
        dept = tables[0].iloc[x]['Undergraduate Engr. Programs']

        if (dept == "Totals:"):
            continue

        df = df.append({'Name': school, 'Level': 'Undergrad', 'Department': dept, 'Year': years[0], 'Total': int(tables[0].iloc[x]['Fresh1st Year'])}, ignore_index=True)
        df = df.append({'Name': school, 'Level': 'Undergrad', 'Department': dept, 'Year': years[1], 'Total': int(tables[0].iloc[x]['Soph2nd Year'])}, ignore_index=True)
        df = df.append({'Name': school, 'Level': 'Undergrad', 'Department': dept, 'Year': years[2], 'Total': int(tables[0].iloc[x]['Junior3rd Year'])}, ignore_index=True)
        df = df.append({'Name': school, 'Level': 'Undergrad', 'Department': dept, 'Year': years[3], 'Total': int(tables[0].iloc[x]['Senior4th/5th Year'])}, ignore_index=True)

    # iterate through remaining tables
    for i in range(1, 5):
        if len(tables[i]) < 4: # doesn't have any majors... for some reason
            print(years[i - 1] + " table for " + school + " doesn't have any majors!")
            continue

        currDept = ''
        for x in range(1, len(tables[i])):
            group = tables[i].iloc[x]['Group']
            if group == 'Men':
                df.loc[(df['Department'] == currDept) & (df['Year'] == years[i - 1]), 'Non-Resident M'] = int(tables[i].iloc[x]['Nonresident Alien'])
                df.loc[(df['Department'] == currDept) & (df['Year'] == years[i - 1]), 'Unknown M'] = int(tables[i].iloc[x]['Unknown'])
                df.loc[(df['Department'] == currDept) & (df['Year'] == years[i - 1]), 'Hispanic M'] = int(tables[i].iloc[x]['Hispanic'])
                df.loc[(df['Department'] == currDept) & (df['Year'] == years[i - 1]), 'American Indian M'] = int(tables[i].iloc[x]['American Indian'])
                df.loc[(df['Department'] == currDept) & (df['Year'] == years[i - 1]), 'Asian M'] = int(tables[i].iloc[x]['Asian'])
                df.loc[(df['Department'] == currDept) & (df['Year'] == years[i - 1]), 'Black M'] = int(tables[i].iloc[x]['Black'])
                df.loc[(df['Department'] == currDept) & (df['Year'] == years[i - 1]), 'Pacific Islander M'] = int(tables[i].iloc[x]['Pacific Islander'])
                df.loc[(df['Department'] == currDept) & (df['Year'] == years[i - 1]), 'White M'] = int(tables[i].iloc[x]['White'])
                df.loc[(df['Department'] == currDept) & (df['Year'] == years[i - 1]), 'TwoorMore M'] = int(tables[i].iloc[x]['Two or More'])
                df.loc[(df['Department'] == currDept) & (df['Year'] == years[i - 1]), 'Total M'] = int(tables[i].iloc[x]['Total'])
            elif group == 'Women':
                df.loc[(df['Department'] == currDept) & (df['Year'] == years[i - 1]), 'Non-Resident F'] = int(tables[i].iloc[x]['Nonresident Alien'])
                df.loc[(df['Department'] == currDept) & (df['Year'] == years[i - 1]), 'Unknown F'] = int(tables[i].iloc[x]['Unknown'])
                df.loc[(df['Department'] == currDept) & (df['Year'] == years[i - 1]), 'Hispanic F'] = int(tables[i].iloc[x]['Hispanic'])
                df.loc[(df['Department'] == currDept) & (df['Year'] == years[i - 1]), 'American Indian F'] = int(tables[i].iloc[x]['American Indian'])
                df.loc[(df['Department'] == currDept) & (df['Year'] == years[i - 1]), 'Asian F'] = int(tables[i].iloc[x]['Asian'])
                df.loc[(df['Department'] == currDept) & (df['Year'] == years[i - 1]), 'Black F'] = int(tables[i].iloc[x]['Black'])
                df.loc[(df['Department'] == currDept) & (df['Year'] == years[i - 1]), 'Pacific Islander F'] = int(tables[i].iloc[x]['Pacific Islander'])
                df.loc[(df['Department'] == currDept) & (df['Year'] == years[i - 1]), 'White F'] = int(tables[i].iloc[x]['White'])
                df.loc[(df['Department'] == currDept) & (df['Year'] == years[i - 1]), 'TwoorMore F'] = int(tables[i].iloc[x]['Two or More'])
                df.loc[(df['Department'] == currDept) & (df['Year'] == years[i - 1]), 'Total F'] = int(tables[i].iloc[x]['Total'])
            else:
                currDept = group

    # replace 'Total O' with actual value
    for x in range(0, len(df)):
        totalf = df.iloc[x]['Total F']
        totalm = df.iloc[x]['Total M']
        total = df.iloc[x]['Total']

        if (totalf + totalm) != total:
            df.iloc[x]['Total O'] = total - (totalf + totalm)
        else:
            df.iloc[x]['Total O'] = 0

    return df


# return a dataframe containing the rows from the grad level of each school
def scrape_grad(school, grad_url, data_columns):
    df = pd.DataFrame(columns=data_columns)
    try:
        tables = pd.read_html(grad_url, header=0)
    except:
        return df

    # find titles of grad programs
    soup = BeautifulSoup(urlopen(grad_url), 'lxml').find(id = 'subPageItem')
    programs = [s.string for s in soup.find_all('p', {'class': 'highlighted'})]

    for i in range(0, len(tables)):
        if len(tables[i]) < 4: # doesn't have any majors... for some reason
            print(programs[i] + " table for " + school + " doesn't have any majors!")
            continue

        currDept = ''
        for x in range(1, len(tables[i])):
            group = tables[i].iloc[x]['Group']
            if group == 'Men':
                # Men row is first, make program rows when we get to one
                df = df.append({'Name': school, 'Level': 'Grad', 'Department': currDept, 'Year': programs[i]}, ignore_index=True)

                df.loc[(df['Department'] == currDept) & (df['Year'] == programs[i]), 'Non-Resident M'] = int(tables[i].iloc[x]['Nonresident Alien'])
                df.loc[(df['Department'] == currDept) & (df['Year'] == programs[i]), 'Unknown M'] = int(tables[i].iloc[x]['Unknown'])
                df.loc[(df['Department'] == currDept) & (df['Year'] == programs[i]), 'Hispanic M'] = int(tables[i].iloc[x]['Hispanic'])
                df.loc[(df['Department'] == currDept) & (df['Year'] == programs[i]), 'American Indian M'] = int(tables[i].iloc[x]['American Indian'])
                df.loc[(df['Department'] == currDept) & (df['Year'] == programs[i]), 'Asian M'] = int(tables[i].iloc[x]['Asian'])
                df.loc[(df['Department'] == currDept) & (df['Year'] == programs[i]), 'Black M'] = int(tables[i].iloc[x]['Black'])
                df.loc[(df['Department'] == currDept) & (df['Year'] == programs[i]), 'Pacific Islander M'] = int(tables[i].iloc[x]['Pacific Islander'])
                df.loc[(df['Department'] == currDept) & (df['Year'] == programs[i]), 'White M'] = int(tables[i].iloc[x]['White'])
                df.loc[(df['Department'] == currDept) & (df['Year'] == programs[i]), 'TwoorMore M'] = int(tables[i].iloc[x]['Two or More'])
                df.loc[(df['Department'] == currDept) & (df['Year'] == programs[i]), 'Total M'] = int(tables[i].iloc[x]['Total'])
            elif group == 'Women':
                df.loc[(df['Department'] == currDept) & (df['Year'] == programs[i]), 'Non-Resident F'] = int(tables[i].iloc[x]['Nonresident Alien'])
                df.loc[(df['Department'] == currDept) & (df['Year'] == programs[i]), 'Unknown F'] = int(tables[i].iloc[x]['Unknown'])
                df.loc[(df['Department'] == currDept) & (df['Year'] == programs[i]), 'Hispanic F'] = int(tables[i].iloc[x]['Hispanic'])
                df.loc[(df['Department'] == currDept) & (df['Year'] == programs[i]), 'American Indian F'] = int(tables[i].iloc[x]['American Indian'])
                df.loc[(df['Department'] == currDept) & (df['Year'] == programs[i]), 'Asian F'] = int(tables[i].iloc[x]['Asian'])
                df.loc[(df['Department'] == currDept) & (df['Year'] == programs[i]), 'Black F'] = int(tables[i].iloc[x]['Black'])
                df.loc[(df['Department'] == currDept) & (df['Year'] == programs[i]), 'Pacific Islander F'] = int(tables[i].iloc[x]['Pacific Islander'])
                df.loc[(df['Department'] == currDept) & (df['Year'] == programs[i]), 'White F'] = int(tables[i].iloc[x]['White'])
                df.loc[(df['Department'] == currDept) & (df['Year'] == programs[i]), 'TwoorMore F'] = int(tables[i].iloc[x]['Two or More'])
                df.loc[(df['Department'] == currDept) & (df['Year'] == programs[i]), 'Total F'] = int(tables[i].iloc[x]['Total'])
            else:
                currDept = group

    # set totals / 0 out total O
    for x in range(0, len(df)):
        totalf = df.iloc[x]['Total F']
        totalm = df.iloc[x]['Total M']
        df.iloc[x]['Total'] = totalf + totalm
        df.iloc[x]['Total O'] = 0

    return df


data_columns = ['Name', 'Level', 'Department', 'Year', 'Non-Resident M', 'Non-Resident F', 'Unknown M', 'Unknown F', 'Hispanic M', 'Hispanic F', 'American Indian M', 'American Indian F', 'Asian M', 'Asian F', 'Black M', 'Black F', 'Pacific Islander M', 'Pacific Islander F', 'White M', 'White F', 'TwoorMore M', 'TwoorMore F', 'Total M', 'Total F', 'Total O', 'Total']

url_list = get_asee_urls('http://profiles.asee.org/profiles?year=2018&commit=Go')
df = pd.DataFrame(columns=data_columns)

for i in range(0, len(url_list)):
    if url_list.iloc[i]['Undergraduate'] != '':
        df = df.append(scrape_undergrad(url_list.iloc[i]['University'], url_list.iloc[i]['Undergraduate'], data_columns), ignore_index=True)

    if url_list.iloc[i]['Graduate'] != '':
        df = df.append(scrape_grad(url_list.iloc[i]['University'], url_list.iloc[i]['Graduate'], data_columns), ignore_index=True)

df.to_csv("asee-profiles-2018.csv", index=False)
