#!/bin/bash

# Create data directory if it doesn't exist
mkdir -p /hadoop/dfs/data

# Wait for namenode to be up
echo "Waiting for namenode to be available..."
while ! nc -z namenode 9000; do
  sleep 2
done
echo "Namenode is up and running."

# Set the DataNode hostname if provided via environment
if [ ! -z "$DATANODE_HOSTNAME" ]; then
  echo "Setting DataNode hostname to $DATANODE_HOSTNAME"
  # Add to hadoop-env.sh
  echo "export HADOOP_OPTS=\"$HADOOP_OPTS -Ddfs.datanode.hostname=$DATANODE_HOSTNAME\"" >> /opt/hadoop/etc/hadoop/hadoop-env.sh
fi

# Wait a bit more to ensure namenode is fully initialized
sleep 5

# Start datanode
echo "Starting datanode..."
hdfs --daemon start datanode

# Check if datanode started successfully
sleep 2
if pgrep -f "proc_datanode" > /dev/null ; then
  echo "Datanode started successfully"
else
  echo "Datanode failed to start. Check logs:"
  cat /opt/hadoop/logs/*datanode*.log
fi

# Keep container running
tail -f /dev/null
