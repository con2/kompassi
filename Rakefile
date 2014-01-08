require 'cucumber/rake/task'

namespace :cucumber do
  Cucumber::Rake::Task.new(:wip) do |t|
    t.cucumber_opts = "--color --tags '@wip'"
  end
end

Cucumber::Rake::Task.new do |t|
  t.cucumber_opts = "--color --tags '~@wip'"
end
