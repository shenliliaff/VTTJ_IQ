from django.views.generic import TemplateView
from django.urls import path
from . import views
from django_filters.views import FilterView
from .filter import audit_info_filter
from .models import is_audit,is_finding,is_action

app_name = 'QtCompetence'
urlpatterns = [
    #管理员页面
    path('admin',views.admin, name='admin'),
    path('',views.home.as_view(), name='home'),
    #员工自评 Competence system
    path('competence_judge',views.competence_judge, name='competence_judge'),
    #经理管理员工评价进度
    path('competence_manage',views.competence_manage.as_view(), name='competence_manage'),
    #经理评价
    path('competence_manager_judge/<int:user_id>',views.competence_manager_judge, name='competence_manager_judge'),
    #更新个人评分最新分数
    path('competence_info_update/<int:pk>',views.competence_info_update.as_view(), name='competence_info_update'),
    #部门经理与厂长数据分析观察页面
    path('competence_analyze',views.competence_analyze, name='competence_analyze'),
    path('login_user',views.login_user.as_view(), name='login_user'),
    path('logout',views.logout_user, name='logout'),
    #个人主页分角色
    path('personal_home',views.personal_home, name='personal_home'),
    path('staff_home/<int:user_id>',views.staff_home, name='staff_home'),
    #audit
    path('audit_home',views.audit_home, name='audit_home'),
    #级联选择audit_body与audit_body_detail
    path('ajax_load_audit_body_detail',views.ajax_load_audit_body_detail, name='ajax_load_audit_body_detail'),
    #audit info create
    path('audit_info_create',views.audit_info_create.as_view(), name='audit_info_create'),
    #audit info update
    path('audit_info_update/<int:pk>',views.audit_info_update.as_view(), name='audit_info_update'),
    #audit info delete
    path('audit_info_delete/<int:pk>',views.audit_info_delete.as_view(), name='audit_info_delete'),
    #audit info list
    path('audit_info_list',views.audit_info_list.as_view(), name='audit_info_list'),
    #级联选择IATF与IATF_Detail
    path('ajax_load_IATF_detail',views.ajax_load_IATF_detail, name='ajax_load_IATF_detail'),
    #finding info create
    path('finding_info_create',views.finding_info_create.as_view(), name='finding_info_create'),
    #finding info update
    path('finding_info_update/<int:pk>',views.finding_info_update.as_view(), name='finding_info_update'),
    #finding info delete
    path('finding_info_delete/<int:pk>',views.finding_info_delete.as_view(), name='finding_info_delete'),
    #finding info list
    path('finding_info_list',views.finding_info_list.as_view(), name='finding_info_list'),
    #action info create
    path('action_info_create',views.action_info_create.as_view(), name='action_info_create'),
    #级联选择audit与finding
    path('ajax_load_finding',views.ajax_load_finding, name='ajax_load_finding'),
    #action info update
    path('action_info_update/<int:pk>',views.action_info_update.as_view(), name='action_info_update'),
    #action info delete
    path('action_info_delete/<int:pk>',views.action_info_delete.as_view(), name='action_info_delete'),
    #action info list
    path('action_info_list',views.action_info_list.as_view(), name='action_info_list'),
    #audit all info list 
    path('audit_all_info_list',views.audit_all_info_list.as_view(), name='audit_all_info_list'),
    #audit export all info export
    path('export_audit_all_info_excel',views.export_audit_all_info_excel, name='export_audit_all_info_excel'),
    #competence all info list 
    path('competence_all_info_list',views.competence_all_info_list.as_view(), name='competence_all_info_list'),
    #competence export all info export
    path('export_competence_all_info_excel',views.export_competence_all_info_excel, name='export_competence_all_info_excel'),
    #部门经理与厂长审核数据分析观察页面
    path('audit_analyze',views.audit_analyze, name='audit_analyze'),
    path('send_email/<int:user_id>',views.send_email, name='send_email'),
    path('contact_us',views.contact_us, name='contact_us'),
    path('FAQ',views.FAQ, name='FAQ'),
    path('api/search',views.api_search, name='api_search'),
]