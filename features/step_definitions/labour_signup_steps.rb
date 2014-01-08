Given /^there is an event that is open for applications$/ do
  manage :tracon9, '--test'
end

When /^I move to sign up for an event$/ do
  click_on 'Tracon 9'
  find('.core-event-view h2').should have_content 'Tracon 9'
end

When /^I fill in the requested extra details$/ do
  pending
end

Then /^I should be signed up for the event$/ do
  pending
end
