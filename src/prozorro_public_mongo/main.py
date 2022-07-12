from prozorro_crawler.main import main
from .tenders import data_handler
import logging

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logger.warning("This command is deprecated. Pls use prozorro_public_mongo.tenders instead")
    main(data_handler)
