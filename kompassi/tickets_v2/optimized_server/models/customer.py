import pydantic

# Paytrail documents max 50 chars for firstName/lastName.
# Dots and pipes are known to cause Paytrail API errors (pipe is documented; dot empirical).
# Block all ASCII punctuation except space, apostrophe and hyphen, plus control chars and DEL.
# Anchors are required: pydantic pattern is an unanchored search, unlike the HTML pattern attribute.
# Must be \A...\z (not \Z) for pydantic's Rust regex engine. Keep the character class in sync
# with namePattern in kompassi-v2-frontend/src/components/tickets/ContactForm.tsx.
CUSTOMER_NAME_PATTERN = r"\A[^\x00-\x1f\x21-\x26\x28-\x2c\x2e\x2f\x3a-\x40\x5b-\x60\x7b-\x7f]+\z"


class Customer(pydantic.BaseModel, frozen=True, populate_by_name=True):
    """
    Arbitrary limits on field lengths to prevent someone putting megabytes of
    hodgepodge in the DB.
    """

    first_name: str = pydantic.Field(
        validation_alias="firstName",
        serialization_alias="firstName",
        max_length=50,
        pattern=CUSTOMER_NAME_PATTERN,
    )
    last_name: str = pydantic.Field(
        validation_alias="lastName",
        serialization_alias="lastName",
        max_length=50,
        pattern=CUSTOMER_NAME_PATTERN,
    )
    email: pydantic.EmailStr = pydantic.Field(
        validation_alias="email",
        serialization_alias="email",
        max_length=300,
    )
    phone: str | None = pydantic.Field(
        validation_alias="phone",
        serialization_alias="phone",
        default="",
        max_length=50,
    )
