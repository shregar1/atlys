from http import HTTPStatus
from typing import Dict

from abstractions.service import IService

from constants.api_status import APIStatus

from dtos.responses.base import BaseResponseDTO

from errors.unexpected_response_error import UnexpectedResponseError

from tasks.scrape.products import scrape_products

from utilities.dictionary import DictionaryUtility


class InitiateScrapeProductsService(IService):

    def __init__(self, urn: str = None, api_name: str = None) -> None:
        super().__init__(urn, api_name)

        self.dictionary_utility = DictionaryUtility(urn=urn)

    async def run(self, data: dict):

        try:

            scrape_products.delay(
                urn=self.urn,
                data=data
            )
            response_payload: Dict[str, str] = {
                "message": "Scraping request peocessing initiated"
            }

            return BaseResponseDTO(
                transactionUrn=self.urn,
                status=APIStatus.SUCCESS,
                responseMessage="Successfully scraped products.",
                responseKey="success_scrape_products_initiated",
                data=self.dictionary_utility.convert_dict_keys_to_camel_case(response_payload)
            )

        except Exception as err:

            self.logger.error(f"Unexpected error occureed while scraping products: {err}")
            raise UnexpectedResponseError(
                responseMessage="Unexpected error occured while scraping products",
                responseKey="error_unexpected_error",
                http_status_code=HTTPStatus.UNPROCESSABLE_ENTITY
            )