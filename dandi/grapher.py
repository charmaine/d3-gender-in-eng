import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

university_data = pd.read_csv('asee-profiles-2018.csv', header=0)
#print(car_data.loc[0]['Name'])
uiuc = university_data.loc[(university_data['Name'] == "University of Illinois at Urbana-Champaign") & (university_data['Level'] == "Undergrad")]
cs = uiuc.loc[uiuc['Department'] == "Computer Science (B.S.)"]
female_years = cs['Total F'].tolist()
male_years = cs['Total M'].tolist()

mit = university_data.loc[(university_data['Name'] == "Massachusetts Institute of Technology") & (university_data['Level'] == "Undergrad")]
mit_cs = mit.loc[mit['Department'] == "Engineer in Computer Science (Eng.)"]
mit_female_years = mit_cs['Total F'].tolist()
mit_male_years = mit_cs['Total M'].tolist()

stanford = university_data.loc[(university_data['Name'] == "Stanford University") & (university_data['Level'] == "Undergrad")]
stanny_cs = stanford.loc[stanford['Department'] == "Computer Science B.S."]
stanny_female_years = stanny_cs['Total F'].tolist()
stanny_male_years = stanny_cs['Total M'].tolist()

berkeley = university_data.loc[(university_data['Name'] == "Stanford University") & (university_data['Level'] == "Undergrad")]
ucb_cs = berkeley.loc[berkeley['Department'] == "Computer Science (B.A.)"]
ucb_female_years = ucb_cs['Total F'].tolist()
ucb_male_years = ucb_cs['Total M'].tolist()

CMU = university_data.loc[(university_data['Name'] == "Carnegie Mellon University") & (university_data['Level'] == "Undergrad")]
CMU_cs = CMU.loc[CMU['Department'] == "Computer Science (B.S.)"]
CMU_female_years = CMU_cs['Total F'].tolist()
CMU_male_years = CMU_cs['Total M'].tolist()

cornellu = university_data.loc[(university_data['Name'] == "Cornell University") & (university_data['Level'] == "Undergrad")]
csCornell = cornellu.loc[cornellu['Department'] == "Computer Science (B.S.)"]
cornell_female_years = csCornell['Total F'].tolist()
cornell_male_years = csCornell['Total M'].tolist()


barWidth = 0.25



#
# barsFuiuc = [freshmanF, sophomoreF, juniorF, seniorF]
# barsFStanford = [stanny_freshmanF, stanny_sophomoreF, stanny_juniorF, stanny_seniorF]
# barsFucb = [ucb_freshmanF, ucb_sophomoreF, ucb_juniorF, ucb_seniorF]
# barsFcmu = [CMU_freshmanF, CMU_sophomoreF, CMU_juniorF, CMU_seniorF]
# barsFcornell = [freshmanFCornell, sophomoreFCornell, juniorFCornell, seniorFCornell]
# barsFmit = [mit_freshmanF, mit_sophomoreF, mit_juniorF, mit_seniorF]
#
# barsMuiuc = [freshmanM, sophomoreM, juniorM, seniorM]
# barsMStanford = [stanny_freshmanM, stanny_sophomoreM, stanny_juniorM, stanny_seniorM]
# barsMucb = [ucb_freshmanM, ucb_sophomoreM, ucb_juniorM, ucb_seniorM]
# barsMcmu = [CMU_freshmanM, CMU_sophomoreM, CMU_juniorM, CMU_seniorM]
# barsMcornell = [freshmanMCornell, sophomoreMCornell, juniorMCornell, seniorMCornell]
# barsMmit = [mit_freshmanM, mit_sophomoreM, mit_juniorM, mit_seniorM]
#

# Set position of bar on X axis
r1 = np.arange(len(female_years))
r2 = [x + barWidth for x in r1]
r3 = [x + barWidth for x in r2]
r4 = [x + barWidth for x in r3]
r5 = [x + barWidth for x in r4]
r6 = [x + barWidth for x in r5]
r7 = [x + barWidth for x in r6]
r8 = [x + barWidth for x in r7]
r9 = [x + barWidth for x in r8]
r10 = [x + barWidth for x in r9]
r11 = [x + barWidth for x in r10]
r12 = [x + barWidth for x in r11]

print(stanny_male_years)
# Make the plot
plt.bar(r1, female_years, color='#FFB816', width=barWidth, edgecolor='white', label='Females at UIUC')
plt.bar(r2, male_years, color='#ff7300', width=barWidth, edgecolor='white', label='Males at UIUC')
plt.bar(r3, stanny_female_years, color='#fa5064', width=barWidth, edgecolor='white', label='Females at Stanford')
plt.bar(r4, stanny_male_years, color='#fc9aa6', width=barWidth, edgecolor='white', label='Males at Stanford')
#plt.bar(r5, ucb_female_years, color='#A9DEF9', width=barWidth, edgecolor='white', label='var5')
#plt.bar(r6, ucb_male_years, color='#D3F8E2', width=barWidth, edgecolor='white', label='var6')
# plt.bar(r7, CMU_female_years, color='#DE8B04', width=barWidth, edgecolor='white', label='var1')
# plt.bar(r8, CMU_male_years, color='#4BAADB', width=barWidth, edgecolor='white', label='var2')
# plt.bar(r9, cornell_female_years, color='#A554D6', width=barWidth, edgecolor='white', label='var3')
# plt.bar(r10, cornell_male_years, color='#E85499', width=barWidth, edgecolor='white', label='var4')
# plt.bar(r11, mit_female_years, color='#E8D951', width=barWidth, edgecolor='white', label='var5')
# plt.bar(r12, mit_male_years, color='#51E88E', width=barWidth, edgecolor='white', label='var6')

# Add xticks on the middle of the group bars
plt.xlabel('group', fontweight='bold')
plt.xticks([r + barWidth for r in range(len(female_years))], ['Freshman', 'Sophomore', 'Junior', 'Senior'])

# Create legend & Show graphic
plt.legend()
plt.show()
