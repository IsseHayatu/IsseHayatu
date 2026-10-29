"""Render every geospatial launch record in a separate Folium map per site.
Markers retain source coordinates. Spiderfy spreads colocated icons only on screen.
"""
from pathlib import Path
import folium,pandas as pd
from folium.plugins import MarkerCluster
from branca.element import Element
ROOT=Path(__file__).parent;OUT=ROOT/'evidence';OUT.mkdir(exist_ok=True)
data=pd.read_csv(ROOT/'data/spacex_launch_geo.csv')
assert len(data)==56
for i,(site,rows) in enumerate(data.groupby('Launch Site'),1):
 lat,lon=map(float,rows[['Lat','Long']].iloc[0]);m=folium.Map(location=[lat,lon],zoom_start=16,max_zoom=18,tiles='OpenStreetMap');m.options['maxZoom']=18
 group=MarkerCluster(spiderfy_on_max_zoom=True,spiderfy_distance_multiplier=1.3,show_coverage_on_hover=False).add_to(m);first=None
 for _,record in rows.iterrows():
  cls=int(record['class']);fl=int(record['Flight Number']);color='#168a84' if cls else '#cc6c52'
  icon=folium.DivIcon(html=f'<div style="width:38px;height:38px;border-radius:50%;border:2px solid white;background:{color};color:white;font:bold 20px Arial;text-align:center;line-height:38px">{fl}</div>',icon_size=(38,38),icon_anchor=(19,19))
  marker=folium.Marker([float(record.Lat),float(record.Long)],icon=icon,tooltip=f'{site} | Flight {fl} | class {cls}',popup=f"{site}<br>Flight {fl}<br>{record['Date']}<br>{record['Landing Outcome']}<br>class {cls}").add_to(group)
  if first is None:first=marker
 m.get_root().script.add_child(Element(f'setTimeout(function(){{var map={m.get_name()};map.panBy([0,-25],{{animate:false}});var p={group.get_name()}.getVisibleParent({first.get_name()});if(p && p.spiderfy)p.spiderfy();}},600);'))
 m.save(OUT/f'site_records_{i}.html');print(site,len(rows),'records',int(rows['class'].sum()),'Class 1')
