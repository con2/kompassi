# kompaq – Outbound AMQP notifications from Kompassi

The `kompaq` application supports outbound notifications from Kompassi using AMQP.

Model-specific fanout exchanges are used. For example `kompassi.access.smtppassword`:

* `kompassi` is the NEW_INSTALLATION_SLUG
* `access` is the app label
* `smtppassword` is the model name
