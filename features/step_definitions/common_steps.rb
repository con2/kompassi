Given /^there is an event that is open for applications$/ do
  manage :tracon9, '--test'
end

Given /^I am not yet logged in$/ do
  visit '/'
  page.title.should == 'ConDB'
end

Given /^I am logged in$/ do
  pending
end
