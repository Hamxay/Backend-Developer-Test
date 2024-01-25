from pydantic import BaseModel


class CreateAddressSchema(BaseModel):
    street: str
    postal_code: str
    city: str
    state: str
    country: str
    lat: float
    lng: float


class AddressSchema(BaseModel):
    id: str  # noqa: A003
    street: str
    postal_code: str
    city: str
    state: str
    country: str
    lat: float
    lng: float

    class Config:
        from_attributes = True
