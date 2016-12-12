#Serving Layer Setup:

After trying several solutions, including flask and django, we found that re:dash was a great interface that had built in modules to cover our needs. 
It's easy to deploy, allows forking queries, runs with a very light footprint, and has built in user controls, caching, and can handle spikes in volumes.

Full implementation details are available at [redash.io](https://redash.io/help-onpremise/setup/setting-up-redash-instance.html)

## 1. Set up an EC2 instance using the re:dash AMI
We used: [ami-3ff16228](https://console.aws.amazon.com/ec2/home?region=us-east-1#LaunchInstanceWizard:ami=ami-3ff16228)
t2.small is enough to host the visualization layer for our data set.
Enable ports 22, 80, and 443


### 2. Check that package loaded correctly:
Go to the AWS Public IP for the EC2 instance
Login to url using: login/pw: admin/admin


## 3.1. Connect via SSH as user ubuntu
Edit /opt/redash/.env to change the default cookie secret password
You'll need to use sudo to have write permissions:
```
sudo vim /opt/redash/.env
```

## 3.2. Set up UI email and password
http://...AWS Public IP URL.../users/me#settings


## 3.3 Google User Authentication
We skipped it because the demo is available without logging in. 
However for private accounts, we'd recommend following the gAuth steps in Users & Google Authentication Setup [Step 3](https://redash.io/help-onpremise/setup/setting-up-redash-instance.html#setup-redash-instance-setup)


## 4. Connect to the postgres table with the data
We used an RDS hosted database because it allows us to use a scalable PstgreSQL database for a reasonable price.
[Amazon RDS](https://console.aws.amazon.com/rds/home?region=us-east-1)

![alt Setup DB Connection](https://github.com/superbb/w205_energy/blob/master/img/redash-setup-db.png "re:dash Setup DB Connection")


## 5. Use Queries to set up and save key queries. 
(Tip: IF you need to copy/reuse a query, use the fork option on the top right corner.)

![alt Make Query](https://github.com/superbb/w205_energy/blob/master/img/redash-make-query.png "re:dash Make Query")


After saving each query, create the visualizations you want to display.

![alt Add Visualizations](https://github.com/superbb/w205_energy/blob/master/img/redash-make-dash.png "re:dash Add Visualizations")


## 6. Create a new dashboard.
Add widgets which will contain the visualizations from the queries.

![alt Make New Dashboard](https://github.com/superbb/w205_energy/blob/master/img/redash-make-dash.png "re:dash Make New Dashboard")


## 7. Use edit dashboard to visually order your widgets.
![alt Make Add Widgets](https://github.com/superbb/w205_energy/blob/master/img/redash-add-widget.png "re:dash Add Widgets")


## 8. Use the public url to display your dashboard publically.
![alt Make Public](https://github.com/superbb/w205_energy/blob/master/img/redash-make-public.png "re:dash Make Public")

