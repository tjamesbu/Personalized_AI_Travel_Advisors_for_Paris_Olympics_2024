import pandas as pd
import wikipedia as wp
from bs4 import BeautifulSoup

html = wp.page("List_of_diplomatic_missions_in_Paris").html()
soup = BeautifulSoup(html, 'lxml')

df_emb = pd.read_html(html)[0]
df_emb['Category']='Embassy'
df_cons = pd.read_html(html)[1]
df_cons['Category']='Consulate'
df_oth = pd.read_html(html)[2]
df_oth['Category']='Other missions or delegations'
df_all = pd.concat([df_emb, df_cons, df_oth])

ref_list_html = soup.find("ol", {"class": "references"})
links = []
for item in ref_list_html.find_all('li'):
    link = item.find('a', class_='external text')
    if link:
        href = link.get('href')
        id = '[' + str(item['id'].split('-')[-1]) + ']'
        links.append({'Website':id, 'WebsiteURL':href})
df_links = pd.DataFrame(links)

df_final = pd.merge(df_all, df_links, on='Website', how='inner')
df_final.reset_index(drop=True)
df_final = df_final[['Country','Category', 'Address','Area','WebsiteURL']].sort_values(by='Country')
df_final.to_csv('diplomatic_missions.csv', index=False, encoding='utf-8')