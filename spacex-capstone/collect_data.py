"""Download the IBM course snapshots and inspect the original API response.
The optional Wikipedia extraction preserves the original historical revision.
The historical endpoint can reject automated requests; failures are recorded.
"""
from pathlib import Path
import requests,pandas as pd,json,io
from bs4 import BeautifulSoup
ROOT=Path(__file__).parent; DATA=ROOT/'data';DATA.mkdir(exist_ok=True)
BASE='https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/'
FILES={name:BASE+'datasets/'+name for name in ['API_call_spacex_api.json','dataset_part_1.csv','dataset_part_2.csv','dataset_part_3.csv','spacex_launch_dash.csv','spacex_launch_geo.csv']}
FILES['Spacex.csv']=BASE+'labs/module_2/data/Spacex.csv'
WIKI='https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922'
def collect():
 for name,url in FILES.items():
  r=requests.get(url,timeout=60);r.raise_for_status();(DATA/name).write_bytes(r.content)
 raw=pd.json_normalize(json.loads((DATA/'API_call_spacex_api.json').read_text()))
 print('Raw API launches:',len(raw));print('First static fire date:',raw.static_fire_date_utc.iloc[0])
 # Single core and payload; use the same historical cutoff as the course.
 selected=raw[(raw.cores.map(len)==1)&(raw.payloads.map(len)==1)].copy()
 selected=selected[pd.to_datetime(selected.date_utc,utc=True)<='2020-11-13T23:59:59Z']
 # Enrichment in the lab resolves rocket/payload/launchpad/core ids with /v4 endpoints.
 # This project uses the provided enriched snapshot to keep results reproducible.
 prepared=pd.read_csv(DATA/'dataset_part_1.csv')
 print('Prepared Falcon 9 launches:',len(prepared))
 status={'wiki_url':WIKI,'enrichment':'IBM prepared course snapshot'}
 r=requests.get(WIKI,timeout=30,headers={'User-Agent':'EducationalCapstone/1.0'})
 status['wiki_http_status']=r.status_code
 if r.ok:
  soup=BeautifulSoup(r.text,'html.parser')
  tables=[t for t in soup.find_all('table') if 'Payload' in t.get_text() and 'Launch' in t.get_text()]
  (DATA/'wiki_launches.html').write_text(r.text)
  for i,t in enumerate(tables):
   try:pd.read_html(io.StringIO(str(t)))[0].to_csv(DATA/f'wiki_table_{i}.csv',index=False)
   except ValueError:pass
  status['title']=soup.title.get_text() if soup.title else None
  status['candidate_tables']=len(tables)
 else:
  status['note']='Historical Wikipedia request blocked; no fresh scrape claimed. Downstream labs use their independent supplied snapshots.'
 (ROOT/'collection_status.json').write_text(json.dumps(status,indent=2))
 print(status)
if __name__=='__main__':collect()
