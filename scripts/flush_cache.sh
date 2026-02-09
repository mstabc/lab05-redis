#!/bin/sh
echo "Flushing Redis cache..."
redis-cli FLUSHALL
echo "Cache cleared."
