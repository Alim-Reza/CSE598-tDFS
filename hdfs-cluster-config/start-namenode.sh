#!/bin/bash

# Make directories if they don't exist
mkdir -p /hadoop/dfs/name

# Format namenode if not already formatted
if [ ! -d "/hadoop/dfs/name/current" ]; then
  echo "Formatting namenode directory"
  hdfs namenode -format
fi

# Start namenode
hdfs --daemon start namenode

# Keep container running
tail -f /dev/null
