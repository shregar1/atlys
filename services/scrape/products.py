import requests

from bs4 import BeautifulSoup
from http import HTTPStatus
import pandas as pd
from typing import Dict

from abstractions.service import IService

from constants.api_status import APIStatus

from dtos.responses.base import BaseResponseDTO

from errors.bad_input_error import BadInputError
from errors.unexpected_response_error import UnexpectedResponseError

from start_utils import db_session

from utilities.dictionary import DictionaryUtility


class ScrapeProductsService(IService):

    def __init__(self, urn: str = None, api_name: str = None) -> None:
        super().__init__(urn, api_name)

        self.dictionary_utility = DictionaryUtility(urn=urn)

    async def __fetch_webpage_text(self, url: str):

        response = requests.get(url)

        if response.status_code == 200:
            html_content = response.text
        else:
            html_content = ""

        return html_content

    async def __scrape_products(self, html_content: str):
        """
        Scrape product information including image URLs from the HTML content
        Returns a pandas DataFrame with product details
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        products = soup.find_all('li', class_='product')
        
        product_data = []
        
        for product in products:
            self.logger.debug("Initialize data dictionary for current product")
            data = {}
            
            self.logger.debug("Get product title")
            title_elem = product.find('h2', class_='woo-loop-product__title')

            self.logger.debug("Get product URL")
            url = title_elem.a['href'] if title_elem else None
            data['url'] = url
            data['title'] = url.strip("/").split("/")[-1].upper()
            
            self.logger.debug("Get product description")
            desc_elem = product.find('div', class_='woocommerce-product-details__short-description')
            data['description'] = desc_elem.text.strip() if desc_elem else None
            
            self.logger.debug("Get product SKU")
            add_to_cart_btn = product.find('a', class_='add_to_cart_button')
            data['sku'] = add_to_cart_btn['data-product_sku'] if add_to_cart_btn else None
            
            self.logger.debug("Get product ID")
            data['product_id'] = add_to_cart_btn['data-product_id'] if add_to_cart_btn else None
            
            self.logger.debug("Get price information")
            price_box = product.find('div', class_='mf-product-price-box')
            if price_box:
                self.logger.debug("Get regular price (if exists)")
                del_price = price_box.find('del')
                if del_price:
                    data['regular_price'] = del_price.text.strip().replace('₹', '').replace(',', '')
                
                self.logger.debug("Get sale price (if exists)")
                ins_price = price_box.find('ins')
                if ins_price:
                    data['sale_price'] = ins_price.text.strip().replace('₹', '').replace(',', '')
                
                self.logger.debug("Get starting price for variable products")
                starting_price = price_box.find('span', class_='starting')
                if starting_price:
                    price_amount = price_box.find('span', class_='woocommerce-Price-amount')
                    data['starting_price'] = price_amount.text.strip().replace('₹', '').replace(',', '') if price_amount else None
            
            self.logger.debug("Get discount percentage")
            discount_elem = product.find('span', class_='onsale')
            if discount_elem:
                discount_text = discount_elem.text.strip()
                data['discount'] = discount_text.split('%')[0].replace('-', '').strip()
            
            self.logger.debug("Check if product is in stock")
            product_class = product.get('class')
            data['in_stock'] = 'outofstock' not in product_class
            
            self.logger.debug("Get image information")
            img_elem = product.find('img', class_='attachment-woocommerce_thumbnail')
            if img_elem:
                self.logger.debug("Get main image URL - handle both lazy-loaded and regular images")
                data['main_image_url'] = img_elem.get('data-lazy-src') or img_elem.get('src')
                
                self.logger.debug("Get all image URLs from srcset")
                srcset = img_elem.get('data-lazy-srcset') or img_elem.get('srcset')
                if srcset:
                    self.logger.debug("Parse srcset attribute to get all image URLs and their sizes")
                    image_urls = []
                    try:
                        for src_item in srcset.split(','):
                            url = src_item.strip().split(' ')[0]
                            image_urls.append(url)
                        data['all_image_urls'] = image_urls
                    except Exception as err:
                        data['all_image_urls'] = None
            
            self.logger.debug("Add to product list")
            product_data.append(data)

        return product_data

    async def run(self, data: dict):

        try:

            products: list = []
            offset: int = data.get("offset")
            limit: int = data.get("limit")
            for i in range(offset, offset+limit+1):

                url = f"https://dentalstall.com/shop/page/{i}/"
                webpage_text: str = await self.__fetch_webpage_text(url=url)
                page_products: list = await self.__scrape_products(html_content=webpage_text)
                products.extend(page_products)

            response_payload: Dict[str, str] = {
                "start_page": offset,
                "end_page": offset+limit,
                "products": products
            }

            return response_payload

        except Exception as err:

            self.logger.error(f"Unexpected error occureed while scraping products: {err}")
            raise UnexpectedResponseError(
                responseMessage="Unexpected error occured while scraping products",
                responseKey="error_unexpected_error",
                http_status_code=HTTPStatus.UNPROCESSABLE_ENTITY
            )