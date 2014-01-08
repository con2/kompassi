module DjangoHelper
  def manage(cmd, *args)
    system 'virtualenv/bin/python', 'manage.py', cmd.to_s, *args
  end
end

World(DjangoHelper)

Before do
  manage :flush, '--noinput'
end