from ...models import Signup


class SignupCertificateProxy(Signup):
    """
    Contains additional methods for Signup used only by the work certificate printing process.
    """

    @property
    def printable_certificate_delivery_address(self):
        """
        We give the users too much freedom in giving their certificate delivery addresses.
        Try to normalize the addresses into a format generally understood by the post office.
        """

        address = self.signup_extra.certificate_delivery_address

        contains_name = self.person.firstname_surname.lower() in address.lower()

        address = address.replace(",", "\n")
        address_lines = address.split("\n")

        if not contains_name:
            address_lines.insert(0, self.person.firstname_surname)

        address_lines = [line.strip() for line in address_lines if line.strip()]

        return "\n".join(address_lines)

    class Meta:
        proxy = True
