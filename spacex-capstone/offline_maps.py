from pathlib import Path
import folium,pandas as pd,json,re,math
R=Path(__file__).parent;g=pd.read_csv(R/'data/spacex_launch_geo.csv');world=json.loads((R/'web_assets/countries.geojson').read_text());countries={'type':'FeatureCollection','features':[f for f in world['features'] if f['properties'].get('ADMIN') in ['United States of America','Canada','Mexico','Cuba','The Bahamas']]}
css=(R/'web_assets/leaflet.css').read_text();js=(R/'web_assets/leaflet.js').read_text()
def save(m,name):
 text=m.get_root().render();text=re.sub(r'<script[^>]+src="[^"]+"[^>]*>\s*</script>','',text);text=re.sub(r'<link[^>]+href="[^"]+"[^>]*>','',text)
 text=text.replace('</head>','<style>'+css+'</style><script>'+js+';window.$=function(s){var t=document.createElement("template");t.innerHTML=s;return [t.content.firstElementChild]};</script></head>');(R/name).write_text(text)
def base(center,zoom):
 m=folium.Map(location=center,zoom_start=zoom,tiles=None,prefer_canvas=True)
 folium.GeoJson(countries,style_function=lambda f:{'fillColor':'#dde6d5','fillOpacity':1,'color':'#8ca4a2','weight':1}).add_to(m)
 folium.map.CustomPane('labels',z_index=650).add_to(m)
 return m
def label(m,coord,text):folium.Marker(coord,icon=folium.DivIcon(html=f'<div style="width:240px;color:#14364a;background:white;font-size:17px;font-weight:bold;padding:4px">{text}</div>'),pane='labels').add_to(m)
sites=g.groupby('Launch Site',as_index=False)[['Lat','Long']].first()
m=base([32,-96],4)
for _,s in sites.iterrows():folium.CircleMarker([s.Lat,s.Long],radius=8,color='#087f8c',fill=True,fill_opacity=1).add_to(m)
label(m,[34.7,-120.7],'VAFB SLC-4E');label(m,[28.7,-80.6],'Cape Canaveral / Kennedy')
save(m,'launch_sites_map.html')
m=base([28.57,-80.61],12)
for _,s in sites[sites.Long>-100].iterrows():
 rows=g[g['Launch Site']==s['Launch Site']];success=int(rows['class'].sum());color='#168a84' if success/len(rows)>.5 else '#cc6c52'
 popup='<b>'+s['Launch Site']+'</b><br>'+str(len(rows))+' launch records, '+str(success)+' successes<br>'+rows[['Date','Landing Outcome']].head(5).to_html(index=False)
 folium.CircleMarker([s.Lat,s.Long],radius=14,color=color,fill=True,fill_opacity=.85,popup=folium.Popup(popup,max_width=430),tooltip=s['Launch Site']).add_to(m)
 label(m,[s.Lat+(-.008 if s['Launch Site']=='CCAFS LC-40' else .004),s.Long+.002],s['Launch Site']+f' ({success}/{len(rows)})')
save(m,'launch_records_map.html')
start=[28.56319718,-80.57682003];m=base(start,12)
refs=json.loads((R/'proximity_results.json').read_text())
folium.CircleMarker(start,radius=8,color='#173f61',fill=True).add_to(m);label(m,start,'CCAFS SLC-40')
for x in refs:
 co=[x['latitude'],x['longitude']];folium.CircleMarker(co,radius=6,color='#d16b35',fill=True).add_to(m);folium.PolyLine([start,co],color='#168a84',weight=2).add_to(m)
 
 if x['reference']=='Titusville reference': label(m,co,'Titusville reference')
m.fit_bounds([start]+[[x['latitude'],x['longitude']] for x in refs]);save(m,'proximity_map.html')
print('Prepared tile-independent Folium maps with Natural Earth boundaries')
