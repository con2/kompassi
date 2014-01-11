module LoginHelper
  def login
    fill_in 'Käyttäjätunnus', with: 'mahti'
    fill_in 'Salasana',       with: 'mahti'
    click_on 'Kirjaudu'
  end
end

World(LoginHelper)

Given /^I am not yet logged in$/ do
  visit '/logout'
  page.title.should == 'ConDB'
end

Given /^I am logged in$/ do
  visit '/login'
  login
end

Then /^I should see the login page$/ do
  page.find('.core-login-view h2').should have_content 'Kirjaudu sisään'
end

When /^I log in$/ do
  login
end

