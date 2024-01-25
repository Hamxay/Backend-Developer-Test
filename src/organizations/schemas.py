from pydantic import ConfigDict, BaseModel


class OrganizationSchema(BaseModel):
    id: int  # noqa: A003
    model_config = ConfigDict(from_attributes=True)
