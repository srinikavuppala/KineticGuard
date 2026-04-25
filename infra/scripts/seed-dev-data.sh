#!/bin/bash
echo "Seeding development database..."
docker-compose exec backend python -m app.utils.seed_dev_data
echo "Dev data seeded!"