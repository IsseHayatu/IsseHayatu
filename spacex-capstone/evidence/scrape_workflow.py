from pathlib import Path
import json,io,re,requests
import pandas as pd
from bs4 import BeautifulSoup
ROOT=Path(__file__).parent
URL='https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches'
def parse_launches(html):
 soup=BeautifulSoup(html,'html.parser');frames=[]
 for table in soup.find_all('table',class_='wikitable'):
  text=table.get_text(' ',strip=True)
  if 'Launch outcome' not in text or 'Booster landing' not in text:continue
  df=pd.read_html(io.StringIO(str(table)))[0]
  if isinstance(df.columns,pd.MultiIndex):df.columns=[' '.join(dict.fromkeys(map(str,x))) for x in df.columns]
  df.columns=[re.sub(r'\[[^\]]*\]','',str(x)).strip() for x in df.columns]
  datecol='Date and time (UTC)'
  mask=df[datecol].astype(str).str.match(r'^(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+20\d{2}')
  df=df[mask].copy()
  for col in df.select_dtypes('object'):df[col]=df[col].astype(str).str.replace(r'\[[^\]]*\]','',regex=True).str.strip()
  df=df.loc[:,~df.columns.str.startswith('Unnamed')].drop_duplicates('Flight No.')
  frames.append(df)
 return soup,pd.concat(frames,ignore_index=True),len(frames)
def main(refresh=False):
 path=ROOT/'wiki_current.html'
 if refresh or not path.exists():
  response=requests.get(URL,timeout=30);response.raise_for_status();path.write_text(response.text)
 soup,data,table_n=parse_launches(path.read_text())
 data.to_csv(ROOT/'wikipedia_scraped_current.csv',index=False)
 status={'url':URL,'http_status':200,'retrieval_date':'2026-10-29','title':soup.title.get_text(),'html_tables':len(soup.find_all('table')),'completed_launch_tables':table_n,'parsed_rows':len(data),'columns':data.columns.tolist(),'historical_revision_http_status':403,'scope_note':'Current page completed launch tables (2025-2026), independent workflow demonstration. Not substituted into the 2010-2020 modeling cohort.'}
 (ROOT/'scraping_evidence.json').write_text(json.dumps(status,indent=2));print(json.dumps(status,indent=2));return data
if __name__=='__main__':main()
