from dtos.requests.apis.base import BaseRequestDTO


class ScrapeProductsRequestDTO(BaseRequestDTO):
    
    offset: int
    limit: int
    callback_url: str