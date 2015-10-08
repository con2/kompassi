from ..helpers import membership_organization_required


def membership_profile_box_context(request):
    return dict()


@membership_organization_required
def membership_apply_view(request, organization):
    raise NotImplementedError()


def membership_profile_view(request):
    raise NotImplementedError()


def membership_organization_box_context(request, organization):
    return dict()
