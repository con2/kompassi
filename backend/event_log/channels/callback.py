def send_update_for_entry(subscription, entry):
    if subscription.channel != "callback":
        raise AssertionError("subscription.channel is not callback")

    subscription.callback(subscription, entry)
