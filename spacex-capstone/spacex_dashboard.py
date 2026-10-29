"""SpaceX success dashboard. Run: python spacex_dashboard.py. Uses course 56-record snapshot."""
from pathlib import Path
import pandas as pd
import plotly.express as px
from dash import Dash,dcc,html,Input,Output
R=Path(__file__).parent
data=pd.read_csv(R/'data/spacex_launch_dash.csv')
app=Dash(__name__)
app.title='SpaceX Launch Success Dashboard'
app.layout=html.Div([
 html.H1('SpaceX Launch Success Dashboard'),
 html.P('Course dashboard snapshot: 56 launch records. Landing success is distinct from mission success.'),
 html.Label('Launch site'),
 dcc.Dropdown(id='site',options=[{'label':'All launch sites','value':'ALL'}]+[{'label':s,'value':s} for s in sorted(data['Launch Site'].unique())],value='ALL',clearable=False),
 html.Label('Payload mass range (kg)'),
 dcc.RangeSlider(id='payload',min=0,max=10000,step=500,value=[0,10000],marks={v:str(v) for v in range(0,10001,2000)},tooltip={'placement':'bottom','always_visible':True}),
 html.Div([dcc.Graph(id='pie'),dcc.Graph(id='scatter')],style={'display':'grid','gridTemplateColumns':'1fr 1fr'}),
 html.P('All-sites pie shows the distribution of successful landings across sites. A selected site shows success versus failure. Both charts respect the payload filter.')
],style={'fontFamily':'Arial','padding':'30px','maxWidth':'1450px','margin':'auto','background':'#f4f7fa','color':'#17394e'})
@app.callback(Output('pie','figure'),Output('scatter','figure'),Input('site','value'),Input('payload','value'))
def charts(site,payload):
 d=data[data['Payload Mass (kg)'].between(payload[0],payload[1])].copy()
 if site!='ALL':d=d[d['Launch Site']==site]
 if site=='ALL':
  p=d[d['class']==1].groupby('Launch Site',as_index=False)['class'].sum()
  pie=px.pie(p,names='Launch Site',values='class',title='Successful landings by launch site')
 else:
  p=d['class'].value_counts().rename_axis('Outcome').reset_index(name='Count');p['Outcome']=p.Outcome.map({0:'Failure / other',1:'Success'})
  pie=px.pie(p,names='Outcome',values='Count',title=f'Landing outcomes: {site}')
 scatter=px.scatter(d,x='Payload Mass (kg)',y='class',color='Booster Version Category',hover_data=['Launch Site','Flight Number'],title='Payload mass and landing outcome',labels={'class':'Landing outcome (0 / 1)'})
 scatter.update_yaxes(tickvals=[0,1],ticktext=['Failure / other','Success'])
 for f in [pie,scatter]:f.update_layout(template='plotly_white',height=540)
 return pie,scatter
if __name__=='__main__':app.run(port=8052,debug=False)
