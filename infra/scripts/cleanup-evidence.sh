#!/bin/bash
echo "Running Phase 2 evidence cleanup (files older than 30 days)..."
docker-compose exec backend python -m app.tasks.maintenance_tasks cleanup_expired_evidence
echo "Cleanup complete!"