#!/bin/sh
# wait-for-db.sh

DB_HOST=$1
shift
CMD="$@"

echo "Waiting for PostgreSQL at $DB_HOST..."

until pg_isready -h "$DB_HOST" -U "$POSTGRES_USER"; do
  echo "Database not ready yet, retrying in 2s..."
  sleep 2
done

echo "PostgreSQL is ready! Starting app..."
exec $CMD
