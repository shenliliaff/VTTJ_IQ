import django_filters as filter
from .models import is_audit,is_action,is_finding,is_user,is_competition_score
class audit_info_filter(filter.FilterSet):
    user=filter.CharFilter(field_name='user__employ_name',lookup_expr='icontains')
    class Meta:
        model = is_audit
        #查询
        fields = ['audit_body','department']

class finding_info_filter(filter.FilterSet):
    finding_content=filter.CharFilter(field_name='finding_content',lookup_expr='icontains')
    class Meta:
        model = is_finding
        #查询
        fields = ['audit','audit_department']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['user'].queryset=is_user.objects.filter(department_id='18')

class action_info_filter(filter.FilterSet):
    user=filter.CharFilter(field_name='user__employ_name',lookup_expr='icontains')
    class Meta:
        model = is_action
        #查询
        fields = ['finding']