import pydantic


class Customer(pydantic.BaseModel, frozen=True):
    """
    Arbitrary limits on field lengths to prevent someone putting megabytes of
    hodgepodge in the DB.
    """

    first_name: str = pydantic.Field(alias="firstName", max_length=100)
    last_name: str = pydantic.Field(alias="lastName", max_length=200)
    email: pydantic.EmailStr = pydantic.Field(alias="email", max_length=300)
    phone: str = pydantic.Field(alias="phone", default="", max_length=50)
