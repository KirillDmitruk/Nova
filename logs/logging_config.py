import logging

logging.basicConfig(
    level=logging.INFO,
    filename="logs/nova.log",
    filemode="w",
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    encoding="utf-8"
)

logger = logging.getLogger(__name__)
