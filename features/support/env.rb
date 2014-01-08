require 'rspec/expectations'
require 'capybara'
require 'capybara/dsl'
require 'capybara/cucumber'
require 'capybara-webkit'
require 'capybara-screenshot'
require 'capybara-screenshot/cucumber'

Capybara.default_selector = :css
Capybara.default_driver = :webkit
Capybara.app_host = "http://localhost:8000"
Capybara.save_and_open_page_path = 'tmp/capybara'
Capybara.default_wait_time = 5 # seconds, default 2
Capybara.ignore_hidden_elements = true