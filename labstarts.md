#ad labstarts here

##script that gets all stuff running

```
wget https://s3.amazonaws.com/ucbdatasciencew205/setup_ucb_complete_plus_postgres.sh
chmod +x ./setup_ucb_complete_plus_postgres.sh
./setup_ucb_complete_plus_postgres.sh

chmod a+rwx /data
sudo mkfs -t ext4 /dev/xvdf

mount -t ext4 /dev/xvdf /data
./setup_ucb_complete_plus_postgres.sh

/root/start-hadoop.sh
/data/start_postgres.sh
/data/start_metastore.sh
```
