from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import ContentType,Group,Permission
from .models import *
from .forms import *
from django.db.models import Q
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django_apscheduler.models import DjangoJobExecution,DjangoJob
#from guardian.models import GroupObjectPermission,UserObjectPermission

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = is_user
        fields = ('user_name','employ_name','email','department','position','is_active', 'is_admin')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    #password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = is_user
        #fields = ('user_name','employ_name','email','department','position','is_active', 'is_admin')
        fields='__all__'

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.password

#覆盖user 自定义鉴权
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('employ_name','user_name','password','department','position', 'is_admin',)
    list_filter = ('is_admin',)
    fieldsets = (
        ('Login info', {'fields': ('user_name',)}),
        ('Personal info', {'fields': ('employ_name',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_name', 'employ_name', 'password1', 'password2'),
        }),
    )
    search_fields = ('user_name','employ_name','id','department__department_name','position__position_name')
    ordering = ('user_name',)
    filter_horizontal = ()

#Now register the new UserAdmin...
admin.site.register(is_user, UserAdmin)
# Register your models here.
class DeptAdmin(admin.ModelAdmin):
    search_fields = ('department_name',)
admin.site.register(is_department,DeptAdmin)
# admin.site.register(is_team)
class PosAdmin(admin.ModelAdmin):
    search_fields = ('position_name',)
admin.site.register(is_position,PosAdmin)

#qualified level过滤器
class LevelFilter(admin.SimpleListFilter):
    title = 'level' #过滤标题显示为"以 英雄性别"
    parameter_name = 'qualified_level' #过滤器使用的过滤字段

    def lookups(self, request, model_admin):
        '''针对字段值设置过滤器的显示效果'''
        return (
            ('No Level', 'No Level'),
            ('basic', 'basic'),
            ('advanced', 'advanced'),
            ('expert', 'expert'),
        )

    def queryset(self, request, queryset):
        '''定义过滤器的过滤动作'''
        if self.value() == 'No Level':
            return r_rules_position.objects.filter(standard_score__icontains=12).all()
        elif self.value() == 'basic':
            return r_rules_position.objects.filter(standard_score__icontains=13).all()
        elif self.value() == 'advanced':
            return r_rules_position.objects.filter(standard_score__icontains=14).all()
        elif self.value() == 'expert':
            return r_rules_position.objects.filter(standard_score__icontains=15).all()
        
class RulesAdmin(admin.ModelAdmin):
    list_display=('competence_id','competence_name','group','scope')
    search_fields = ('competence_name','group','scope')
    ordering=('competence_id',)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "trainer":
            kwargs["queryset"] = is_user.objects.filter(Q(department_id=18)|Q(department_id=6)).order_by('employ_name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
admin.site.register(is_competition_rule,RulesAdmin)
class ScoreAdmin(admin.ModelAdmin):
    search_fields = ('user__employ_name',)
admin.site.register(is_competition_score,ScoreAdmin)
# class UsersAdmin(admin.StackedInline):
#     model = is_user

# @admin.register(r_level)
# class levelAdmin(admin.ModelAdmin):
#     inlines=[UsersAdmin,]
   
class R_RulesAdmin(admin.ModelAdmin):
    list_display=('id','position_name','rules_name','qualified_level')
    def position_name(self,obj):
        return obj.position
    def rules_name(self,obj):
        return obj.rules
    def qualified_level(self,obj):
        if obj.standard_score == 12:
            return 'No Level'
        elif obj.standard_score == 13:
            return 'basic'
        elif obj.standard_score == 14:
            return 'advanced'
        elif obj.standard_score == 15:
            return 'expert'
        else:
            return 'others'
    ordering=('id',)
    search_fields=('id','position__position_name','rules__competence_name',)
    list_filter = (LevelFilter,)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "position_name":
            kwargs["queryset"] = is_position.objects.filter(Q(department_id=18)|Q(department_id=6))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
admin.site.register(r_rules_position,R_RulesAdmin)
#Audit
admin.site.register(is_audit)
admin.site.register(is_audit_department)
admin.site.register(is_audit_body)
admin.site.register(is_audit_body_detail)
admin.site.register(is_audit_type)
admin.site.register(is_IATF)
admin.site.register(is_IATF_detail)
admin.site.register(is_finding)


# admin.site.register(UserObjectPermission)
# admin.site.register(GroupObjectPermission)
# admin.site.register(ContentType)
# class UserAdmin(admin.StackedInline):
#     model = User
# class ContactAdmin(admin.StackedInline):
#     model = Contact

# class UserProfileAdmin(admin.ModelAdmin):
#     inlines = [ UserAdmin, ContactAdmin ]