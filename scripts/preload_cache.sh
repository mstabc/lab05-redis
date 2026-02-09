#!/bin/sh
echo "Preloading Redis cache..."
for i in $(seq 0 9999); do
  redis-cli SET "user:$i" "value_$i" EX 60 > /dev/null
done
echo "Done."
