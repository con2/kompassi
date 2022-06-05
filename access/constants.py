# event manager permissions are set to expire this many days after event ends
CBAC_VALID_AFTER_EVENT_DAYS = 180

# when a superuser overrides permissions, this is how many minutes the temporary permissions last
CBAC_SUDO_VALID_MINUTES = 20

# these claims are used, if present, when sudoing. Note that sudo cannot give you a {} permission
CBAC_SUDO_CLAIMS = ["organization", "event", "app"]
