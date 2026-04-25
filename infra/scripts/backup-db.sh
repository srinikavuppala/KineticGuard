#!/bin/bash
echo "Backing up PostgreSQL database..."
docker-compose exec db pg_dump -U $POSTGRES_USER $POSTGRES_DB > backup_$(date +%Y%m%d_%H%M%S).sql
echo "Backup complete!"