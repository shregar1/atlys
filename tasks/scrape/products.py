import time
from uuid import uuid4
import asyncio

from services.scrape.products import ScrapeProductsService

from repositories.product import ProducRepository, Product

from start_utils import celery, logger, db_session

@celery.task(name='tasks.scrape.products.scrape_products')
def scrape_products(urn: str, data: dict) -> None:

    logger.debug("Scraping products")
    response_payload =  asyncio.run(ScrapeProductsService(
        urn=urn
    ).run(data=data))
    logger.debug("Scraped products")

    products = response_payload.get("products", [])

    product_repository: ProducRepository = ProducRepository(
        urn=urn,
        session=db_session
    )

    count = 0
    for record in products:

        product: Product = product_repository.retrieve_record_by_title(
            title=record.get("title")
        )

        if product:

            logger.debug("Product already exists")
            continue
        
        logger.debug("Creating product record")
        product: Product = Product(
            urn=str(uuid4()),
            title=record.get("title"),
            url=record.get("url"),
            description=record.get("description"),
            sku=record.get("sku"),
            product_id=record.get("product_id"),
            regular_price=record.get("regular_price"),
            sale_price=record.get("sale_price"),
            starting_price=record.get("starting_price"),
            discount=record.get("discount"),
            in_stock=record.get("in_stock"),
            main_image_url=record.get("main_image_url"),
            all_image_urls=record.get("all_image_urls")
        )

        product = product_repository.create_record(product=product)
        logger.debug(f"Created product record: {product.id}")

        count += 1

    print(db_session)
    print(db_session.__dict__)
    return {
        "start_page": response_payload.get("start_page"),
        "end_page": response_payload.get("end_page"),
        "count": count
    }