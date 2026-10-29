-- launch_sites
SELECT DISTINCT Launch_Site FROM SPACEXTBL ORDER BY Launch_Site;

-- ccaf_sites
SELECT DISTINCT Launch_Site FROM SPACEXTBL WHERE Launch_Site LIKE 'CCA%';

-- nasa_payload
SELECT SUM(PAYLOAD_MASS__KG_) AS total_kg FROM SPACEXTBL WHERE Customer = 'NASA (CRS)';

-- f9v11_average
SELECT AVG(PAYLOAD_MASS__KG_) AS average_kg FROM SPACEXTBL WHERE Booster_Version LIKE 'F9 v1.1%';

-- first_ground_success
SELECT MIN(Date) AS first_date FROM SPACEXTBL WHERE Landing_Outcome = 'Success (ground pad)';

-- drone_4to6t
SELECT Date,Booster_Version,PAYLOAD_MASS__KG_ FROM SPACEXTBL WHERE Landing_Outcome = 'Success (drone ship)' AND PAYLOAD_MASS__KG_ > 4000 AND PAYLOAD_MASS__KG_ < 6000;

-- mission_outcomes
SELECT Mission_Outcome,COUNT(*) AS launches FROM SPACEXTBL GROUP BY Mission_Outcome;

-- max_payload_boosters
SELECT DISTINCT Booster_Version,PAYLOAD_MASS__KG_ FROM SPACEXTBL WHERE PAYLOAD_MASS__KG_ = (SELECT MAX(PAYLOAD_MASS__KG_) FROM SPACEXTBL);

-- drone_failures_2015
SELECT strftime('%m',Date) AS month,Booster_Version,Launch_Site FROM SPACEXTBL WHERE Landing_Outcome = 'Failure (drone ship)' AND strftime('%Y',Date) = '2015';

-- landing_rank
SELECT Landing_Outcome,COUNT(*) AS launches FROM SPACEXTBL WHERE Date BETWEEN '2010-06-04' AND '2017-03-20' GROUP BY Landing_Outcome ORDER BY launches DESC;

-- by_site
SELECT Launch_Site,COUNT(*) AS launches,SUM(CASE WHEN Mission_Outcome='Success' THEN 1 ELSE 0 END) AS mission_successes FROM SPACEXTBL GROUP BY Launch_Site;