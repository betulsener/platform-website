from .models import Setting

def SettingList(request):
    '''
    try:
        context=Setting.objects.get()
    except Setting.DoesNotExist:
        context = None
         
    return {'setting' : context}
    
    '''

    context = Setting.objects.first()
    return{'setting':context}