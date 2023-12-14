run socker-streaming
docker exec -it spark-master /bin/bash
 docker exec -it spark-master spark-submit \
--master spark://spark-master:7077 \
--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 \
jobs/spark-streaming.py