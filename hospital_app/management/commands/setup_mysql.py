#!/usr/bin/env python
import os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import connection


class Command(BaseCommand):
    help = "Initialize MySQL schema and data from combined_schema_and_data.sql"

    def add_arguments(self, parser):
        parser.add_argument(
            '--sql-file',
            default='combined_schema_and_data.sql',
            help='Path to SQL file relative to project root',
        )

    def handle(self, *args, **options):
        sql_rel_path = options['sql_file']
        sql_path = os.path.join(settings.BASE_DIR, sql_rel_path)

        if not os.path.exists(sql_path):
            raise CommandError(f"SQL file not found: {sql_path}")

        self.stdout.write(f"Reading SQL from: {sql_path}")
        with open(sql_path, 'r', encoding='utf-8') as f:
            raw_sql = f.read()

        # Remove comment lines and accumulate statements split by semicolons
        statements = []
        current = []
        for line in raw_sql.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith('--'):
                continue
            current.append(stripped)
            if stripped.endswith(';'):
                stmt = ' '.join(current).rstrip(';')
                statements.append(stmt)
                current = []
        if current:
            statements.append(' '.join(current))

        executed = 0
        with connection.cursor() as cursor:
            for stmt in statements:
                try:
                    cursor.execute(stmt)
                    executed += 1
                except Exception as e:
                    # Log and continue so a single failure doesn't stop all
                    self.stdout.write(self.style.WARNING(
                        f"Failed statement: {stmt[:120]}...\nError: {e}"
                    ))

        self.stdout.write(self.style.SUCCESS(
            f"Completed MySQL setup. Executed {executed} statements from {sql_rel_path}."
        ))
