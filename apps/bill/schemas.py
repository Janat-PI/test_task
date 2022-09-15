from datetime import date

from pydantic import BaseModel, validator


class Data(BaseModel):
    client_name: str
    org: str
    sum_: int
    date: date
    service: str

    @validator("service")
    def service_check(cls, v):
        if "-" in v:
            raise ValueError("service not valid")
        return v

    # @validator("sum_")
    # def sum_check(cls, v):
    #     try:
    #         v = int(v)
    #     except:
    #         raise ValueError("sum not valid")
    #     return v
    # @validator("date")
    # def date(cls, v):
        
    




