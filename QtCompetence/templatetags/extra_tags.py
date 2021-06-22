from django import template
from QtCompetence.models import is_user

register = template.Library()

@register.filter(name='competenceListGroup')
def competenceListGroup(arg):  # 把传递过来的参数arg替换为'~'
    if arg == None:
        return ""
    if arg == 1:
        return 'Methodology & Tool'
    if arg == 2:
        return 'Technical'
    if arg == 3:
        return 'Specialized'
    if arg == 4:
        return 'Soft Skills'
    if arg == 20:
        return 'Methodology'
    if arg == 21:
        return 'Tool'
@register.filter(name='competenceListScope')
def competenceListScope(arg): 
    if arg == 5:
        return 'New Hire/Transferred'
    if arg == 6:
        return 'Formal'
    if arg == 7:
        return 'All'
    if arg == None:
        return ""
@register.filter(name='competenceListTrainingType')
def competenceListTrainingType(arg): 
    if arg == 8:
        return 'Monthly'
    if arg == 9:
        return 'Quarterly'
    if arg == 10:
        return 'Bi-Monthly'
    if arg == 11:
        return 'Others'
    if arg == None:
        return ""
@register.filter(name='competenceListScore')
def competenceListScore(arg): 
    if arg == 12:
        return '0'
    if arg == 13:
        return '1'
    if arg == 14:
        return '2'
    if arg == 15:
        return '3'
    if arg == None:
        return "未评价"

@register.filter(name='managerJudge')
def managerJudge(arg): 
    if arg == None:
        return "未评价"
    else:
        return arg

@register.filter(name='competenceListReference')
def competenceListReference(arg): 
    if arg == None:
        return ''
    else:
        return arg[:30]

@register.filter(name='competenceListTrainer')
def competenceListTrainer(arg):
    if arg == None:
        return ''
    else:
        return is_user.objects.filter(id=arg)[0].employ_name

@register.filter(name='personalHome')
def personalHome(arg):  # 把传递过来的参数arg替换为'~'
    if type(arg) == str:
        return arg
    else:
        if arg == 12:
            return '0'
        elif arg == 13:
            return '1'
        elif arg == 14:
            return '2'
        elif arg == 15:
            return '3'
        elif arg == None:
            return '未评价'
        else:
            return arg

@register.filter(name='auditInfoList')
def auditInfoList(arg):  # 把传递过来的参数arg替换为'~'
    if arg == 16:
        return 'internal'
    if arg == 17:
        return 'external'

@register.filter(name='findingInfoList')
def auditInfoList(arg):  # 把传递过来的参数arg替换为'~'
    if arg == 18:
        return 'Major Nonconfirming'
    if arg == 19:
        return 'Minor Nonconfirming'
    if arg == 20:
        return 'OFI'

#competence rules
@register.filter(name='competenceRules')
def competenceRules(arg):  # 把传递过来的参数arg替换为'~'
    if arg == 1:
        return 'Quality Management System'
    if arg == 4:
        return 'Customer Specific Requirements'
    if arg == 5:
        return 'ESD'
    if arg == 6:
        return 'IPC610'
    if arg == 8:
        return 'Communication skills'
    if arg == 9:
        return 'IMT'
    if arg == 10:
        return 'P FMEA'
    if arg == 11:
        return 'Control Plan'
    if arg == 12:
        return 'VDA6.3'
    if arg == 13:
        return 'VDA6.5'
    if arg == 14:
        return '6 Sigma'
    if arg == 15:
        return 'SPC'
    if arg == 16:
        return 'MSA'
    if arg == 17:
        return 'Minitab'
    if arg == 18:
        return 'PPAP'
    if arg == 19:
        return 'Jidoka'
    if arg == 20:
        return 'QT'
    if arg == 21:
        return 'Product knowledge' 
    if arg == 22:
        return 'Problem Solving'
    if arg == 23:
        return 'CQTS'
    if arg == 24:
        return 'Change Management'
    if arg == 25:
        return 'Yokoten'
    if arg == 27:
        return 'LPA'
    if arg == 28:
        return 'MLC'
    if arg == 29:
        return 'APQP/PLC'
    if arg == 30:
        return 'Customer Portal'
    if arg == 31:
        return 'Data base&Programme'
    if arg == 32:
        return 'Project Management Skills'
    if arg == 33:
        return 'Language skills'
    if arg == 34:
        return 'DOE'
    if arg == 35:
        return 'VDA FFA'
    if arg == 36:
        return 'Warranty Concept'
    else:
        return 'new item'