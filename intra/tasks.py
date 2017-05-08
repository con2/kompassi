from celery import shared_task


@shared_task(ignore_result=True)
def privileges_form_save(team_member_id, cleaned_data):
    from .models import TeamMember
    from .forms import PrivilegesForm

    team_member = TeamMember.objects.get(id=team_member_id)
    PrivilegesForm._save(team_member, cleaned_data)
