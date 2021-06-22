from django import forms
from django.forms import ModelForm,widgets
from django.core.exceptions import ValidationError
# 自定义鉴权对应的创建以及修改用户
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import is_user,is_competition_score,is_audit,is_finding,is_action,is_IATF,is_IATF_detail
from django.db.models import Q

class user_login_form(forms.Form):
    user_name = forms.RegexField(
        r'^([a-zA-Z0-9]{4,16}$)|(([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$)|(^1[3456789]\d{9})$',
        min_length=5,
        label='UserName',
        strip=True,
        error_messages={
            "required": "账户名不能为空",
            "invalid": "账户格式错误",
            "min_length": "账户最短5位",
        },
        widget=widgets.TextInput({'placeholder': 'CA2020', })
    )

    # user_pwd = forms.RegexField(
    #     # 这里正则匹配验证要求密码了里面包含字母、数字
    #     r'^([a-zA-Z0-9]{4,16}$)|(^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[!@#$\%\^\&\*\(\)])[0-9a-zA-Z!@#$\%\^\&\*\(\)]{4,32}$)',
    #     help_text='密码包含字母,数字至少四位',
    #     min_length=2,
    #     max_length=32,
    #     label='Password',
    #     widget=forms.PasswordInput({'placeholder': 'windows登录名 uia3321'}),
    #     error_messages={
    #         "required": "密码不能为空",
    #         "invalid": "密码必须包括字母,数字",
    #         "min_length": "密码的长度不能小于4个字符",
    #         "max_length": "密码长度不能大于32个字符"
    #     }
    # )

    user_pwd = forms.CharField(
        help_text='密码包含字母,数字至少四位',
        min_length=2,
        max_length=32,
        label='Password',
        widget=forms.PasswordInput({'placeholder': 'windows登录名 uia3321'}),
        error_messages={
            "required": "密码不能为空",
            "invalid": "密码必须包括字母,数字",
            "min_length": "密码的长度不能小于4个字符",
            "max_length": "密码长度不能大于32个字符"
        }
    )

    def clean(self):
        user_name = self.cleaned_data.get('user_name')
        user_pwd = self.cleaned_data.get('user_pwd')
        qtUserName = is_user.objects.filter(user_name=user_name)
        qtUserPwd = is_user.objects.filter(password=user_pwd)
        qtExist = is_user.objects.filter(Q(user_name=user_name) & Q(password=user_pwd))
        if not qtUserName:
            raise ValidationError({'user_name': '无效账户'})
        elif not qtExist:
            raise ValidationError({'user_pwd': '您输入的用户名与密码不匹配'})
        else:
            return self.cleaned_data
        


class judgeForm(forms.Form):
    score = forms.ChoiceField(
        label='',
        choices=(
            (12, '0'),
            (13, '1'),
            (14, '2'),
            (15, '3'),
        ),
        widget=widgets.Select(attrs={'class':'score'})
    )
# queryset=is_competition_score.objects.extra(select={"create_time": "DATE_FORMAT(create_time, '%%Y-%%m-%%d %%H:%%i')"}).values_list('create_time',flat=True),
# competence_analyze
class selectTime(forms.Form):
    time = forms.ModelChoiceField(
        label='自评时间筛选:',
        queryset=is_competition_score.objects.extra(select={"create_time": "DATE_FORMAT(create_time, '%%Y-%%m')"}).values_list('create_time',flat=True).distinct(),
    )

class selectFindingTime(forms.Form):
    audit_time = forms.ModelChoiceField(
        label='筛选条件:',
        queryset=is_audit.objects.extra(select={"audit_date": "DATE_FORMAT(audit_date, '%%Y-%%m')"}).values_list('audit_date',flat=True).distinct(),
    )

#personal_home
class correctionForm(forms.Form):
    correction_choice = forms.ChoiceField(
        label='',
        choices=(
            (16,'Training'),
            (17,'Self-Learning'),
            (18,'Job-Rotation'),
            (19,'On-Job-Coach'),
            (20,'Leading-Project'),
            (21,'Others'),
        ),
        widget=widgets.Select(attrs={'class':'score'})
    )

#is_audit
class auditCreateForm(forms.ModelForm):
    class Meta:
        model=is_audit
        fields = ['audit_date', 'department', 'audit_body','audit_body_detail', 'audit_scope', 'audit_type','line','user']

    def __init__(self, *args, **kwargs):
        super(auditCreateForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset=is_user.objects.filter(department_id='18')
        self.fields['line'].required=False

#is_finding
class findingCreateForm(forms.ModelForm):
    class Meta:
        model=is_finding
        exclude=('user',)

    def __init__(self, *args, **kwargs):
        super(findingCreateForm, self).__init__(*args, **kwargs)
        self.fields['IATF_detail'].queryset=is_IATF_detail.objects.none()
        self.fields['audit'].queryset=is_audit.objects.all().order_by('-audit_date')
        if 'IATF' in self.data:
            try:
                IATF_id=int(self.data.get('IATF'))
                self.fields['IATF_detail'].queryset=is_IATF_detail.objects.filter(IATF_id=IATF_id).order_by('IATF_detail_title_ch')
            except(ValueError,TypeError):
                #ingore empty IATF
                pass
        elif self.instance.pk:
            self.fields['IATF_detail'].queryset=self.instance.IATF.IATF_detail_IATF.order_by('IATF_detail_title_ch')

#is_action
class actionCreateForm(forms.ModelForm):
    audit=forms.ModelChoiceField(queryset=is_audit.objects.all(),label='审核信息')
    class Meta:
        model=is_action
        fields = ['due_date', 'actual_date', 'audit','finding','rootCause','correction','action_content','user']
    def __init__(self, *args, **kwargs):
        super(actionCreateForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset=is_user.objects.filter(department_id='18')
        self.fields['due_date'].required=False
        self.fields['actual_date'].required=False
        self.fields['rootCause'].required=False
        self.fields['correction'].required=False
        self.fields['action_content'].required=False
        self.fields['finding'].queryset=is_finding.objects.all().order_by('-audit__audit_date')
    