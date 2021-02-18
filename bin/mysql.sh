docker run \
--rm \
-v $PWD/data/mysql:/var/lib/mysql \
-p 3306:3306 \
-e MYSQL_ALLOW_EMPTY_PASSWORD=true \
mysql