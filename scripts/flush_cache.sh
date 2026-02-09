#!/bin/sh
echo "Flushing Redis cache..."
docker exec -it redis redis-cli FLUSHALL
echo "Cache cleared."
