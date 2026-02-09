#!/bin/sh
echo "Simulating random read load..."
while true; do
  docker exec -it redis redis-cli GET "$((RANDOM % 10000))" > /dev/null
done
