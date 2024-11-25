from fastapi import Request
from fastapi.responses import JSONResponse
from http import HTTPStatus

from abstractions.controller import IController

from constants.api_lk import APILK
from constants.api_status import APIStatus
from constants.payload_type import RequestPayloadType

from dtos.requests.apis.scrape_products import ScrapeProductsRequestDTO
from dtos.responses.base import BaseResponseDTO


from errors.bad_input_error import BadInputError
from errors.unexpected_response_error import UnexpectedResponseError

from services.apis.scrape_products import InitiateScrapeProductsService

from utilities.dictionary import DictionaryUtility


class ScrapeProductsController(IController):

    def __init__(self, urn: str = None) -> None:
        super().__init__(urn)
        self.api_name = APILK.COMPLIANCE_CHECK
        self.payload_type = RequestPayloadType.JSON

    async def post(self, request: Request, request_payload: ScrapeProductsRequestDTO):

        self.logger.debug("Fetching request URN")
        self.urn = request.state.urn
        self.logger = self.logger.bind(urn=self.urn, api_name=self.api_name)
        self.dictionary_utility = DictionaryUtility(urn=self.urn)

        try:

            self.logger.debug("Validating request")
            self.request_payload = request_payload.model_dump()
            
            await self.validate_request(
                request=request
            )
            self.logger.debug("Validated request")

            self.logger.debug("Running scrape product service")
            response_dto: BaseResponseDTO = await InitiateScrapeProductsService(
                urn=self.urn,
                api_name=self.api_name
            ).run(
                data=self.request_payload
            )

            self.logger.debug("Preparing response metadata")
            http_status_code = HTTPStatus.OK
            self.logger.debug("Prepared response metadata")

        except (BadInputError, UnexpectedResponseError) as err:

            self.logger.error(f"{err.__class__} error occured while scrape product: {err}")
            self.logger.debug("Preparing response metadata")
            response_dto: BaseResponseDTO = BaseResponseDTO(
                transactionUrn=self.urn,
                status=APIStatus.FAILED,
                responseMessage=err.responseMessage,
                responseKey=err.responseKey,
                data={},
                error={}
            )
            http_status_code = err.http_status_code
            self.logger.debug("Prepared response metadata")

        except Exception as err:

            self.logger.error(f"{err.__class__} error occured while scrape product: {err}")

            self.logger.debug("Preparing response metadata")
            response_dto: BaseResponseDTO = BaseResponseDTO(
                transactionUrn=self.urn,
                status=APIStatus.FAILED,
                responseMessage="Failed to check compliance",
                responseKey="error_internal_server_error",
                data={},
                error={}
            )
            http_status_code = HTTPStatus.INTERNAL_SERVER_ERROR
            self.logger.debug("Prepared response metadata")

        return JSONResponse(
            content=response_dto.to_dict(),
            status_code=http_status_code
        )