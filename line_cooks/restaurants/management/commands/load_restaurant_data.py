from django.core.management.base import BaseCommand
from restaurants.data_loader import load_data_from_csv
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = (
        "Batch ETL process for extracting, parsing, and loading restaurant hours data"
    )

    def add_arguments(self, parser):
        parser.add_argument("input_file", nargs=1, type=str)

    def handle(self, *args, **options):
        input_path = options["input_file"].pop()
        row_count = load_data_from_csv(input_path)
        logger.info(f"ETL complete. {row_count} rows added")
