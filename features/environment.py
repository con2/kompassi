import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'turska.settings'


def before_all(context):
    # from django.core.management import setup_environ
    # from turska import settings
    # setup_environ(settings)

    from django.test.simple import DjangoTestSuiteRunner
    context.runner = DjangoTestSuiteRunner()

    from south.management.commands import patch_for_test_db_setup
    patch_for_test_db_setup()


def before_scenario(context, scenario):
    context.runner.setup_test_environment()
    context.old_db_config = context.runner.setup_databases()


def after_scenario(context, scenario):
    context.runner.teardown_databases(context.old_db_config)
    context.runner.teardown_test_environment()
