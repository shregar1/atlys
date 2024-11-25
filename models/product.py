from sqlalchemy import Column, Integer, String, Float, Boolean, Text, JSON
from sqlalchemy.ext.declarative import declarative_base

from start_utils import Base


class Product(Base):
    __tablename__ = 'product'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    urn = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    url = Column(String(2048), nullable=False)
    description = Column(Text, nullable=True)
    sku = Column(String(100), nullable=True)
    product_id = Column(String(100), nullable=True)
    regular_price = Column(Float, nullable=True)
    sale_price = Column(Float, nullable=True)
    discount = Column(Float, nullable=True)
    in_stock = Column(Boolean, nullable=False, default=True)
    main_image_url = Column(String(2048), nullable=True)
    all_image_urls = Column(JSON, nullable=True)
    starting_price = Column(Float, nullable=True)

    def __repr__(self):
        return f"<Product(title='{self.title}', url='{self.url}', regular_price={self.regular_price}, sale_price={self.sale_price})>"