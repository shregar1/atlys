from fastapi import APIRouter

from controllers.apis.scrape_products import ScrapeProductsController

from start_utils import logger

router = APIRouter(prefix="/apis")

logger.debug(f"Registering {ScrapeProductsController.__name__} route.")
router.add_api_route(
    path="/scrape_product",
    endpoint=ScrapeProductsController().post,
    methods=["POST"]
)
logger.debug(f"Registered {ScrapeProductsController.__name__} route.")