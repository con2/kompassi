module LoginHelper
  def login
    click_on 'Kirjaudu sisään...'
    fill_in 'Käyttäjätunnus', with: known_users[:ahto][:username]
    fill_in 'Salasana',       with: known_users[:ahto][:password]
    click_on 'Kirjaudu'
  end
end

World(LoginHelper)

Given /^I am not yet logged in$/ do
  visit '/'
  page.title.should == 'ConDB'
end

Given /^I am logged in$/ do
  visit '/'
  login
end

Then /^I should see the login page$/ do
  page.find('.core-login-view h2').should have_content 'Kirjaudu sisään'
end

When /^I log in$/ do
  login
end

