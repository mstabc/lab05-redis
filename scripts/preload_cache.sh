#!/bin/sh
echo "Preloading Redis cache..."
for i in $(seq 0 9999); do
  docker exec redis redis-cli SET "$i" "value_$i" EX 60 > /dev/null
done
echo "Done."
