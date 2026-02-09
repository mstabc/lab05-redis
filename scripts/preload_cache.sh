#!/bin/sh

echo "Preloading Redis cache..."

docker exec redis sh -c '
for i in $(seq 0 9999); do
  redis-cli SET "$i" "value_$i" EX 60
done
' > /dev/null

echo "Done."
