#!/bin/bash
if [ -z "$1" ]; then echo "Usage: ./restore-db.sh <backup_file.sql>"; exit 1; fi
echo "Restoring database from $1..."
docker-compose exec -T db psql -U $POSTGRES_USER $POSTGRES_DB < $1
echo "Restore complete!"