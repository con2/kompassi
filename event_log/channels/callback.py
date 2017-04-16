def send_update_for_entry(subscription, entry):
    assert subscription.channel == 'callback'

    subscription.callback(subscription, entry)
