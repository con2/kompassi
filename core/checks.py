from collections import defaultdict


class CheckBase(object):
    @property
    def name(self):
        return self.__class__.__name__

    def get_objects(self, **opts):
        raise NotImplemented('get_objects')

    def check(self, obj, **opts):
        raise NotImplemented('check')

    def fix(self, obj, problem, **opts):
        # cannot fix
        return False

    def _check(self, obj, fix=False, **opts):
        problem = self.check(obj)

        if problem and fix:
            fix_result = self.fix(obj, problem, **opts)
        else:
            fix_result = None

        if problem:
            print "  *", obj, problem, fix_result

        return obj, problem, fix_result

    def _run(self, **opts):
        return [self._check(obj, **opts) for obj in self.get_objects(**opts)]


# app_label -> check_name -> CheckClass
check_registry = defaultdict(dict)


def register_check(app_label, check):
    check_registry[app_label][check.name] = check


def autodiscover_checks(app_labels=None):
    from importlib import import_module

    if app_labels is None:
        from django.conf import settings
        app_labels = settings.INSTALLED_APPS

    for app_label in app_labels:
        try:
            import_module('{app_label}.checks'.format(app_label=app_label))
        except ImportError:
            pass


def run_checks(app_labels=None, **opts):
    if app_labels is None:
        app_labels = check_registry.keys()

    for app_label in app_labels:
        print "Running checks for", app_label
        for check_name, check in check_registry[app_label].iteritems():
            print "-", check_name
            check._run(**opts)