from pathlib import Path
import pandas as pd,numpy as np,json,sqlite3,warnings
from sklearn.model_selection import train_test_split,GridSearchCV,StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score,confusion_matrix,precision_score,recall_score,f1_score
from sklearn.dummy import DummyClassifier
warnings.filterwarnings('ignore')
R=Path(__file__).parent;D=R/'data'
d=pd.read_csv(D/'dataset_part_2.csv');d['Year']=pd.to_datetime(d.Date).dt.year
x=pd.read_csv(D/'dataset_part_3.csv');y=d.Class.to_numpy()
tr,te=train_test_split(np.arange(len(d)),test_size=.2,random_state=2)
cv=StratifiedKFold(5,shuffle=True,random_state=2)
configs={
'Logistic regression':(LogisticRegression(max_iter=3000),{'model__C':[.01,.1,1,10]}),
'SVM':(SVC(),{'model__C':[.01,.1,1,10,100],'model__gamma':[.001,.01,.0316227766,.1,1],'model__kernel':['linear','rbf','sigmoid']}),
'Decision tree':(DecisionTreeClassifier(random_state=2),{'model__criterion':['gini','entropy'],'model__max_depth':[2,4,6,8,12,None],'model__min_samples_leaf':[1,2,4],'model__min_samples_split':[2,5,10]}),
'KNN':(KNeighborsClassifier(),{'model__n_neighbors':[3,5,7,9,11],'model__weights':['uniform','distance'],'model__p':[1,2]})}
results=[];predictions={}
for name,(model,params) in configs.items():
 search=GridSearchCV(Pipeline([('scale',StandardScaler()),('model',model)]),params,cv=cv,scoring='accuracy',n_jobs=1)
 search.fit(x.iloc[tr],y[tr]);pred=search.predict(x.iloc[te]);predictions[name]=pred.tolist()
 row={'model':name,'cv_accuracy':search.best_score_,'cv_std':search.cv_results_['std_test_score'][search.best_index_],'test_accuracy':accuracy_score(y[te],pred),'precision':precision_score(y[te],pred,zero_division=0),'recall':recall_score(y[te],pred),'f1':f1_score(y[te],pred),'params':search.best_params_,'confusion_matrix':confusion_matrix(y[te],pred).tolist()};results.append(row);print(name,row,flush=True)
best=max(results,key=lambda r:r['cv_accuracy']);dummy=DummyClassifier(strategy='most_frequent').fit(x.iloc[tr],y[tr]);baseline=accuracy_score(y[te],dummy.predict(x.iloc[te]))
# Lab-compatible global-standardization comparison, clearly separate from the main pipeline.
xs=StandardScaler().fit_transform(x)
svc=GridSearchCV(SVC(),{'kernel':['linear','rbf','poly','sigmoid'],'C':np.logspace(-3,3,5),'gamma':np.logspace(-3,3,5)},cv=10)
svc.fit(xs[tr],y[tr]);lab={'svm_params':svc.best_params_,'cv_accuracy':svc.best_score_,'test_accuracy':svc.score(xs[te],y[te])}
# SQL task snapshot has 101 records and a different time window.
sql_df=pd.read_csv(D/'Spacex.csv')
for col in sql_df.select_dtypes('object'):
 sql_df[col]=sql_df[col].str.strip()
con=sqlite3.connect(':memory:');sql_df.to_sql('SPACEXTBL',con,index=False)
queries={
'launch_sites':'SELECT DISTINCT Launch_Site FROM SPACEXTBL ORDER BY Launch_Site',
'ccaf_sites':"SELECT DISTINCT Launch_Site FROM SPACEXTBL WHERE Launch_Site LIKE 'CCA%'",
'nasa_payload':"SELECT SUM(PAYLOAD_MASS__KG_) AS total_kg FROM SPACEXTBL WHERE Customer = 'NASA (CRS)'",
'f9v11_average':"SELECT AVG(PAYLOAD_MASS__KG_) AS average_kg FROM SPACEXTBL WHERE Booster_Version LIKE 'F9 v1.1%'",
'first_ground_success':"SELECT MIN(Date) AS first_date FROM SPACEXTBL WHERE Landing_Outcome = 'Success (ground pad)'",
'drone_4to6t':"SELECT Date,Booster_Version,PAYLOAD_MASS__KG_ FROM SPACEXTBL WHERE Landing_Outcome = 'Success (drone ship)' AND PAYLOAD_MASS__KG_ > 4000 AND PAYLOAD_MASS__KG_ < 6000",
'mission_outcomes':"SELECT Mission_Outcome,COUNT(*) AS launches FROM SPACEXTBL GROUP BY Mission_Outcome",
'max_payload_boosters':"SELECT DISTINCT Booster_Version,PAYLOAD_MASS__KG_ FROM SPACEXTBL WHERE PAYLOAD_MASS__KG_ = (SELECT MAX(PAYLOAD_MASS__KG_) FROM SPACEXTBL)",
'drone_failures_2015':"SELECT strftime('%m',Date) AS month,Booster_Version,Launch_Site FROM SPACEXTBL WHERE Landing_Outcome = 'Failure (drone ship)' AND strftime('%Y',Date) = '2015'",
'landing_rank':"SELECT Landing_Outcome,COUNT(*) AS launches FROM SPACEXTBL WHERE Date BETWEEN '2010-06-04' AND '2017-03-20' GROUP BY Landing_Outcome ORDER BY launches DESC",
'by_site':"SELECT Launch_Site,COUNT(*) AS launches,SUM(CASE WHEN Mission_Outcome='Success' THEN 1 ELSE 0 END) AS mission_successes FROM SPACEXTBL GROUP BY Launch_Site"}
sql={k:pd.read_sql_query(q,con).to_dict('records') for k,q in queries.items()}
(R/'sql_analysis.sql').write_text('\n\n'.join('-- '+k+'\n'+q+';' for k,q in queries.items()))
summary={'rows':len(d),'dates':[d.Date.min(),d.Date.max()],'positives':int(y.sum()),'class_counts':d.Class.value_counts().sort_index().to_dict(),'sites':d.groupby('LaunchSite').Class.agg(['count','sum','mean']).reset_index().to_dict('records'),'orbits':d.groupby('Orbit').Class.agg(['count','sum','mean']).reset_index().to_dict('records'),'yearly':d.groupby('Year').Class.agg(['count','mean']).reset_index().to_dict('records'),'results':results,'best_model':best['model'],'baseline_test_accuracy':baseline,'test_indices':te.tolist(),'test_labels':y[te].tolist(),'predictions':predictions,'train_n':len(tr),'test_n':len(te),'lab_replication':lab,'sql':sql,'queries':queries,'sql_n':len(sql_df)}
(R/'analysis_results.json').write_text(json.dumps(summary,indent=2,default=lambda o:o.item() if hasattr(o,'item') else str(o)))
print('BEST',best['model'],'baseline',baseline,'LAB',lab,'SQL',sql,flush=True)
