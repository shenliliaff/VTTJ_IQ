from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser,PermissionsMixin
from .validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.conf import settings
import datetime
from django.db.models import Q

#select JOB_CODE_ID,JOB_TITLE,INUSE from OEE.ETF_Dim_JobCode where INUSE='Y' order by JOB_CODE_ID;
class is_position(models.Model):
    position_id = models.IntegerField(verbose_name="职位编号")
    position_name = models.CharField(max_length=100,verbose_name="职位名称")
    create_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.position_name

#SELECT DEPARTMENTKEY,DEPARTMENTNAME,INUSE,MANAGER_ID from ir_dimdepartment  where INUSE = 'Y' order by DEPARTMENTKEY;
class is_department(models.Model):
    department_id = models.IntegerField(verbose_name="部门编号")
    department_name = models.CharField(max_length=30,verbose_name="部门名称")
    create_time = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.department_name

#自定义auth user并鉴权
class is_userManager(BaseUserManager):
    def create_user(self, user_name,employ_name, email, password=None):
        #数据均为同步而来无需创建新管理员，直接将对应is_admin字段赋值为1即可
        global user
        if not user_name:
            raise ValueError('Users must have a user_name')
        else:
            user = is_user.objects.filter(user_name=user_name)
        if user:
            return user
        else:
            print('User not exist')
    
    def create_superuser(self,user_name,employ_name, email, password=None):
        #数据均为同步而来无需创建新管理员，直接将对应is_admin字段赋值为1即可
        global user
        if not user_name:
            raise ValueError('Users must have a user_name')
        else:
            user = is_user.objects.filter(user_name=user_name)
        if user:
            user.update(is_admin=1)
            return user
        else:
            print('User not exist')

#SELECT SYS_NAME(password),BADGE_NO(user_name), USER_NAME,EMAIL_ID,DEPARTMENTKEY,JOB_CODE_ID FROM IR_DIMUSER WHERE DEPARTMENTKEY='542' AND INUSE='Y';
class is_user(AbstractBaseUser,PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    user_id = models.IntegerField(verbose_name="用户编号")
    user_name = models.CharField(
        verbose_name="登录名",
        max_length=20,
        help_text=('Required. 20 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        unique=True,
        error_messages={
            'unique': ("A user with that 员工ID already exists."),
        },
    )
    employ_name = models.CharField(max_length=50,verbose_name="姓名")
    #这里需要拼接字符串并对空数据进行一下处理
    email = models.EmailField(verbose_name='邮箱地址',max_length=255,null=True,blank=True)
    department = models.ForeignKey(is_department,on_delete=models.CASCADE)
    position = models.ForeignKey(is_position,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    create_time = models.DateTimeField(default=timezone.now)
    objects = is_userManager()

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['employ_name','password','email']
    

    def __str__(self):
        return self.employ_name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        super().has_perm(perm,obj)
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

def get_anonymous_user_instance(is_user):
    return is_user(user_id=100001,password='NO BADGE',user_name='Anonymous',employ_name='AnonymousUser',email='NO EMAIL_ID',department_id=10000,position_id=10000)

class is_competition_rule(models.Model):
    group_choice = (
        (1, 'Methodology&Tool'),
        (2, 'Technical'),
        (3, 'Specialized'),
        (4, 'Soft Skills'),
        (20, 'Methodology'),
        (21, 'Tool'),
    )
    scope_choice = (
        (5, 'New Hire/Transferred'),
        (6, 'Formal'),
        (7, 'All')
    )
    training_type_choice = (
        (8, 'Monthly'),
        (9, 'Quarterly'),
        (10, 'Bi-Monthly'),
        (11, 'Others')
    )
    
    competence_id = models.AutoField(primary_key=True,verbose_name="评价规则编号")
    competence_name = models.CharField(max_length=500,verbose_name="技能名称")
    group = models.IntegerField(choices=group_choice, verbose_name="技能分类")
    scope = models.IntegerField(choices=scope_choice, verbose_name="面向对象",null=True,blank=True)
    basic_content = models.TextField(max_length=1000,verbose_name="基本水平要求")
    advanced_content = models.TextField(max_length=1000,verbose_name="高级水平要求")
    expert_content = models.TextField(max_length=1000,verbose_name="专家水平要求")
    trainer = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,verbose_name="培训师",null=True,blank=True)
    #blank=True admin级别可为空 null=True,blank=True数据库级别可为空
    training_type = models.IntegerField(choices=training_type_choice, verbose_name="培训频次",null=True,blank=True)
    reference = models.CharField(max_length=500,verbose_name="参考文件",null=True,blank=True)
    create_time = models.DateTimeField(default=timezone.now)
    position = models.ManyToManyField(is_position,through='r_rules_position')

    def __str__(self):
        return self.competence_name

class r_rules_position(models.Model):
    standard_score_choice = (
        (12, '0'),
        (13, '1'),
        (14, '2'),
        (15, '3'),
    )
    standard_score = models.IntegerField(choices=standard_score_choice, verbose_name="Qualified level")
    position = models.ForeignKey(is_position,on_delete=models.CASCADE)
    rules = models.ForeignKey(is_competition_rule,on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        position_name=is_position.objects.filter(id=self.position_id)[0].position_name
        competence_name=is_competition_rule.objects.filter(competence_id=self.rules_id)[0].competence_name
        return '职位：'+position_name+'对应'+competence_name+'的第'+str(self.id)+'条关系'


#员工层级关系表，全部为直接report的主管领导
#select USER_NAME,JOB_CODE_ID,LEVEL_1_R,LEVEL_2_R,LEVEL_3_R,LEVEL_4_R from ir_dimUser WHERE INUSE='Y'
class r_level(models.Model):
    level_id = models.AutoField(primary_key=True,verbose_name="层级关系编号")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, verbose_name="员工权限编号",related_name="user_permission")
    L1 = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, verbose_name="第一层关系",related_name="L1_user")
    L2 = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, verbose_name="第二层关系",related_name="L2_user")
    L3 = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, verbose_name="第三层关系",related_name="L3_user")
    L4 = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, verbose_name="第四层关系",related_name="L4_user")
    create_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '层级关系编码为:'+str(self.level_id)

class is_competition_score(models.Model):
    score_choice = (
        (12, '0'),
        (13, '1'),
        (14, '2'),
        (15, '3'),
    )
    # correction_choice = (
    #     (16,'Training'),
    #     (17,'Self-Learning'),
    #     (18,'Job-Rotation'),
    #     (19,'On-Job-Coach'),
    #     (20,'Leading-Project'),
    #     (21,'Others')
    # )
    assessment_id = models.AutoField(primary_key=True,verbose_name="个人能力得分编号")
    self_assessment = models.IntegerField(choices=score_choice, verbose_name="自评分数")
    manager_assessment = models.IntegerField(choices=score_choice, verbose_name="经理分数",null=True,blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    competence = models.ForeignKey(is_competition_rule,on_delete=models.CASCADE)
    self_gap = models.IntegerField(verbose_name="自评差距")
    # self_correction = models.IntegerField(choices=correction_choice, verbose_name="个人改进措施",null=True,blank=True)
    # self_correction_detail=models.CharField(max_length=400,verbose_name="个人改进措施详情",null=True,blank=True)
    manager_gap = models.IntegerField(verbose_name="经理评价差距",null=True,blank=True)
    # manager_correction = models.IntegerField(choices=correction_choice, verbose_name="经理改进措施",null=True,blank=True)
    # manager_correction_detail=models.CharField(max_length=400,verbose_name="经理改进措施详情",null=True,blank=True)
    create_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        user_name=is_user.objects.filter(id=self.user_id)[0].employ_name
        competence_name=is_competition_rule.objects.filter(competence_id=self.competence_id)[0].competence_name
        return user_name+"的规则: "+str(self.competence)+"的分数"

#Audit
#1.	审核主体信息表is_ audit_body
class is_audit_body(models.Model):
    audit_body_id=models.AutoField(primary_key=True,verbose_name="审核主体编号")
    audit_body_name=models.CharField(max_length=200,verbose_name="审核主体名称")
    create_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.audit_body_name
    
#2.	审核主体信息详情表is_ audit_body_detail
class is_audit_body_detail(models.Model):
    audit_body_detail_id=models.AutoField(primary_key=True,verbose_name="审核主体信息详情编号")
    audit_body_detail_name=models.CharField(max_length=200,verbose_name="审核主体信息详情名称")
    audit_body=models.ForeignKey(is_audit_body,on_delete=models.CASCADE,verbose_name="审核主体")
    create_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.audit_body_detail_name

#3.	审核类型信息is_audit_type
class is_audit_type(models.Model):
    audit_type_id=models.AutoField(primary_key=True,verbose_name="审核类型编号")
    audit_type_name=models.CharField(max_length=200,verbose_name="审核类型名称")
    create_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.audit_type_name

#4.IATF条款is_IATF
class is_IATF(models.Model):
    IATF_id=models.AutoField(primary_key=True,verbose_name="条款编号")
    IATF_title_ch=models.TextField(max_length=500,verbose_name="IATF条款标题中文")
    IATF_content_ch=models.TextField(max_length=2000,verbose_name="IATF条款内容中文")
    IATF_title_en=models.TextField(max_length=500,verbose_name="IATF条款标题英文")
    IATF_content_en=models.TextField(max_length=2000,verbose_name="IATF条款内容英文")
    create_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.IATF_title_ch

#5.IATF条款详情is_IATF_detail
class is_IATF_detail(models.Model):
    IATF_detail_id=models.AutoField(primary_key=True,verbose_name="条款详情编号")
    IATF_detail_title_ch=models.TextField(max_length=500,verbose_name="IATF条款详情标题中文")
    IATF_detail_content_ch=models.TextField(max_length=2000,verbose_name="IATF条款详情内容中文")
    IATF_detail_title_en=models.TextField(max_length=500,verbose_name="IATF条款详情标题英文")
    IATF_detail_content_en=models.TextField(max_length=2000,verbose_name="IATF条款详情内容英文")
    IATF=models.ForeignKey(is_IATF,on_delete=models.CASCADE,verbose_name="IATF条款",related_name="IATF_detail_IATF")
    create_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.IATF_detail_title_ch

#问题内容责任部门表
class is_audit_department(models.Model):
    audit_department_id=models.AutoField(primary_key=True,verbose_name="审核责任部门编号")
    audit_department_name=models.CharField(max_length=200,verbose_name="审核责任部门名称")
    create_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.audit_department_name

#6.审核信息表
class is_audit(models.Model):
    scope_choice = (
        (16, 'internal'),
        (17, 'external'),
    )
    audit_id=models.AutoField(primary_key=True,verbose_name="审核内容编号")
    audit_date=models.DateTimeField(verbose_name="审核日期",default=timezone.now)
    department=models.ForeignKey(is_audit_department,on_delete=models.CASCADE,verbose_name="部门")
    audit_body=models.ForeignKey(is_audit_body,on_delete=models.CASCADE,verbose_name="审核主体")
    audit_body_detail=models.ForeignKey(is_audit_body_detail,on_delete=models.CASCADE,verbose_name="审核主体详情")
    audit_scope = models.IntegerField(choices=scope_choice,verbose_name="审核类型")
    audit_type=models.ForeignKey(is_audit_type,on_delete=models.CASCADE,verbose_name="审核类型信息")
    line=models.CharField(max_length=100,verbose_name="线体/产品",null=True,blank=True)
    create_time = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, verbose_name="负责人",related_name="user_pk")

    class Meta:
        ordering=('-audit_date',)

    def __str__(self):
        return str(self.audit_date)[:10]+' 部门为：'+self.department.audit_department_name+' 审核类型为：'+str(self.audit_type)+' 线体/产品为: '+ str(self.line)
    

#8.审核不符合项信息表is_finding
class is_finding(models.Model):
    weight_choice = (
        (18, 'Major Nonconfirming'),
        (19, 'Minor Nonconfirming'),
        (20, 'OFI')
    )
    finding_id=models.AutoField(primary_key=True,verbose_name="不符合项内容编号")
    audit=models.ForeignKey(is_audit,on_delete=models.CASCADE,verbose_name="审核信息")
    finding_content=models.TextField(max_length=2000,verbose_name="问题内容")
    audit_department=models.ForeignKey(is_audit_department,on_delete=models.CASCADE,verbose_name="问题责任部门")
    IATF=models.ForeignKey(is_IATF,on_delete=models.CASCADE,verbose_name="IATF条款")
    IATF_detail=models.ForeignKey(is_IATF_detail,on_delete=models.CASCADE,verbose_name="IATF详细条款")
    weight=models.IntegerField(choices=weight_choice,verbose_name="问题类型")
    create_time = models.DateTimeField(default=timezone.now,verbose_name="创建日期")
    #记录填写人
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, verbose_name="负责人")

    class Meta:
        ordering=('-audit__audit_date',)

    def __str__(self):
        return self.finding_content[:100]

    

#7.纠正措施is_action
class is_action(models.Model):
    action_id=models.AutoField(primary_key=True,verbose_name="纠正措施编号")
    #responsible=models.CharField(max_length=200,verbose_name="负责人")
    #department=models.ForeignKey(is_department,on_delete=models.CASCADE,verbose_name="部门")
    due_date = models.DateTimeField(default=timezone.now,verbose_name="纠正措施截止日期",null=True,blank=True)
    actual_date = models.DateTimeField(null=True,blank=True,verbose_name="实际纠正措施日期")
    create_time = models.DateTimeField(default=timezone.now,verbose_name="创建日期")
    finding = models.ForeignKey(is_finding, verbose_name="对应问题", on_delete=models.CASCADE)
    action_content = models.TextField(max_length=2000,verbose_name="纠正措施",null=True,blank=True)
    rootCause=models.TextField(max_length=2000,verbose_name="根本原因",null=True,blank=True)
    correction=models.TextField(max_length=2000,verbose_name="纠正",null=True,blank=True)
    #负责人
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, verbose_name="负责人")

    class Meta:
        ordering=('-finding__audit__audit_date',)

    def __str__(self):
        return self.action_content[:100]




# class is_BusinessUnit(modes.Model):
#     BU_id = models.AutoField(primary_key=True,verbose_name="分厂编号")
#     BU_name = models.CharField(max_length=30,verbose_name="分厂名称")
#     BU_type = models.CharField(max_length=20,verbose_name="分厂类型")
# create_time = models.DateTimeField(default=timezone.now)

#     def __str__(self):
#         return self.BU_name

# class is_team(models.Model):
#     team_id = models.AutoField(primary_key=True,verbose_name="团队编号")
#     team_name = models.CharField(max_length=30,verbose_name="团队名称")
# create_time = models.DateTimeField(default=timezone.now)

#     def __str__(self):
#         return self.team_name