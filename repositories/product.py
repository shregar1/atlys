from datetime import datetime, timezone
from sqlalchemy.orm import Session

from models.product import Product

from abstractions.repository import IRepository


class ProducRepository(IRepository):

    def __init__(self, urn:str = None, api_name:str = None, session:Session = None):
        super().__init__(urn, api_name)
        self.urn = urn
        self.api_name = api_name
        self.session = session

        if not self.session:
            raise RuntimeError("DB session not found")
        
    def create_record(self, product: Product) -> Product:

        start_time = datetime.now(timezone.utc)
        self.session.add(product)
        self.session.commit()

        end_time = datetime.now(timezone.utc)
        execution_time = end_time - start_time
        self.logger.info(f"Execution time: {execution_time} seconds")

        return product


    def retrieve_record_by_id(self, id: str) -> Product:

        start_time = datetime.now(timezone.utc)
        record = self.session.query(Product).filter(Product.id == id).first()
        end_time = datetime.now(timezone.utc)
        execution_time = end_time - start_time
        self.logger.info(f"Execution time: {execution_time} seconds")

        return record if record else None
    
    def retrieve_record_by_title(self, title: str) -> Product:

        start_time = datetime.now(timezone.utc)
        record = self.session.query(Product).filter(Product.title == title).first()
        end_time = datetime.now(timezone.utc)
        execution_time = end_time - start_time
        self.logger.info(f"Execution time: {execution_time} seconds")

        return record if record else None

    def retrieve_record_by_urn(self, urn: str) -> Product:

        start_time = datetime.now(timezone.utc)
        record = self.session.query(Product).filter(Product.urn == urn).first()
        end_time = datetime.now(timezone.utc)
        execution_time = end_time - start_time
        self.logger.info(f"Execution time: {execution_time} seconds")

        return record if record else None