from pathlib import Path
import pandas as pd,json,folium,math,requests,re
from folium.plugins import MarkerCluster,MousePosition
R=Path(__file__).parent;D=R/'data'
g=pd.read_csv(D/'spacex_launch_geo.csv');sites=g.groupby('Launch Site',as_index=False)[['Lat','Long']].first()
# Folium maps preserve all source records. Identical launch coordinates cluster naturally.
m=folium.Map(location=[32,-96],zoom_start=4,tiles='OpenStreetMap',width='100%',height='100%')
for _,s in sites.iterrows():
 folium.CircleMarker([s.Lat,s.Long],radius=9,color='#067a84',fill=True,fill_opacity=.9,tooltip=s['Launch Site']).add_to(m)
 folium.Marker([s.Lat,s.Long],icon=folium.DivIcon(html=f'<div style="width:180px;font-size:15px;font-weight:bold;background:white;padding:3px">{s["Launch Site"]}</div>')).add_to(m)
m.save(R/'launch_sites_map.html')
m2=folium.Map(location=[28.57,-80.6],zoom_start=10,tiles='OpenStreetMap')
cluster=MarkerCluster(name='Launch records').add_to(m2)
for _,r in g.iterrows():
 folium.Marker([r.Lat,r.Long],tooltip=f'Flight {r["Flight Number"]}: {r["Launch Site"]}',popup=f'{r["Date"]}: {r["Landing Outcome"]}',icon=folium.Icon(color='green' if r['class']==1 else 'red',icon='info-sign')).add_to(cluster)
folium.LayerControl().add_to(m2);m2.save(R/'launch_records_map.html')
# Reference points are manually selected illustrative coordinates, not nearest-feature estimates.
site=sites[sites['Launch Site']=='CCAFS SLC-40'].iloc[0] if 'CCAFS SLC-40' in sites['Launch Site'].tolist() else sites.iloc[0]
start=[float(site.Lat),float(site.Long)]
refs={'Coastline reference':[28.56367,-80.57163], 'Road reference':[28.5632,-80.6000],'Rail reference':[28.5720,-80.5850],'Titusville reference':[28.6122,-80.8076]}
def hav(a,b):
 lat1,lon1,lat2,lon2=map(math.radians,[*a,*b]);return 6371*2*math.asin(math.sqrt(math.sin((lat2-lat1)/2)**2+math.cos(lat1)*math.cos(lat2)*math.sin((lon2-lon1)/2)**2))
prox=[];m3=folium.Map(location=start,zoom_start=12,tiles='OpenStreetMap')
folium.Marker(start,tooltip='CCAFS SLC-40',icon=folium.Icon(color='blue')).add_to(m3)
for name,coord in refs.items():
 dist=hav(start,coord);prox.append({'reference':name,'latitude':coord[0],'longitude':coord[1],'distance_km':round(dist,3)})
 folium.Marker(coord,tooltip=f'{name}: {dist:.2f} km',popup='Illustrative manually selected reference, not verified nearest feature.').add_to(m3)
 folium.PolyLine([start,coord],color='#0b8593',weight=2,tooltip=f'{dist:.2f} km straight line').add_to(m3)
m3.fit_bounds([start,*refs.values()]);MousePosition().add_to(m3);m3.save(R/'proximity_map.html')
(R/'proximity_results.json').write_text(json.dumps(prox,indent=2))
print('Maps created; proximity references',prox,flush=True)
# Preserve a clean audit of all dataset sizes and scope.
print('Geospatial sites',sites.to_dict('records'),flush=True)
