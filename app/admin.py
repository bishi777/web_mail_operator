from django.contrib import admin
from .models import *
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.admin import UserAdmin


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'registration_subscribe_date',  'is_active', 'check_mail']
    fields = ['gmail_account', 'gmail_account_password', 'user_email', 'h_schedule_time', 'p_schedule_time', 'registration_subscribe_date', 'is_active', 'check_mail']  # 表示・編集可能なフィールドを指定
    
    # 任意でクエリセットを制限
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    # スーパーユーザーでない場合、特定のフィールドを隠す
    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if not request.user.is_superuser:
            fields = [field for field in fields if field not in ('id', 'user', 'h_schedule_time', 'p_schedule_time', 'registration_subscribe_date', 'is_active', 'check_mail_happymail', 'check_mail_pcmax')]
        return fields
admin.site.register(UserProfile, UserProfileAdmin)

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'ユーザーオプション'

class UserAdmin(UserAdmin):
    list_display = ('username', 'is_active', 'get_registration_subscribe_date')  
    # 表示するフィールドを定義
    fieldsets = (
        (None, {'fields': (
            'username', 'password', 'email', 'is_staff', 
            'is_superuser', 'user_permissions', 'is_active', 
            'last_login', 'date_joined'
        )}),
    )
    inlines = (UserProfileInline,)

    # registration_subscribe_dateを取得するメソッド
    def get_registration_subscribe_date(self, obj):
        return obj.userprofile.registration_subscribe_date if hasattr(obj, 'userprofile') else None
    get_registration_subscribe_date.short_description = '課金日'  # 管理画面での表示名を設定


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class PcmaxAdmin(admin.ModelAdmin):
    list_display = ('name', 'login_id', 'post_title', 'is_active','memo')  # 表示するフィールドを指定
    # 編集可能なフィールドを指定（必要に応じて）
    fields = (
        'name', 'user_id', 'login_id', 'password',   'post_title', 'post_content', 'return_foot_message','mail_img',
        'fst_mail', 'second_message', 'condition_message', 'mail_address', 'gmail_password',
        'date_of_birth', 'self_promotion', 
        'height', 'body_shape', 'blood_type', 'activity_area', 'detail_activity_area', 'profession', 
        'freetime', 'car_ownership', 'smoking', 'ecchiness_level', 'sake', 'process_before_meeting', 
        'first_date_cost', 'travel', 'birth_place', 'education', 'annual_income', 'roommate', 
        'marry', 'child', 'housework', 'sociability', 
        'memo','is_active'
              )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        
        return qs.filter(user_id=request.user)
    
    
    def get_fields(self, request, obj=None):
        # スーパーユーザーでない場合、idとuser_idを表示しない
        fields = super().get_fields(request, obj)
        if not request.user.is_superuser:
            fields = [field for field in fields if field not in ('id', 'user_id')]
        return fields
    
    def get_list_display(self, request):
        # スーパーユーザーのみ user_id を表示
        if request.user.is_superuser:
            # return ['user_id'] + self.list_display
            return ['user_id'] + list(self.list_display) 
            
        return self.list_display
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # 新しいオブジェクトの場合のみ
            obj.user_id = request.user
        # UserProfileが存在しない場合は作成
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        # is_activeがTrueの場合に制限を適用
        if obj.is_active and not user_profile.lifted_account_number:
            active_count = Pcmax.objects.filter(user_id=obj.user_id, is_active=True).count()
            if active_count >= 8:
                messages.error(request, 'You cannot have more than 8 active Pcmax records.')
                return
            
        super().save_model(request, obj, form, change)

admin.site.register(Pcmax, PcmaxAdmin)


class HappymailAdmin(admin.ModelAdmin):
    list_display = ['name', 'post_title', 'login_id', 'is_active', 'memo']
    fields = [
        'user_id', 'name', 'login_id', 'password', 'post_title', 
        'post_contents', 'return_foot_message', 'fst_message', 'second_message', 
        'chara_image', "age", "activity_area", "detail_activity_area",
        "birth_place", "blood_type", "constellation", "height",
        "style", "looks", "cup", "job", "education", "holiday",
        "relationship_status", "having_children", "intention_to_marry",
        "smoking", "sake", "car_ownership","roommate", 
        "brothers_and_sisters", "until_we_met","date_expenses", 
        'is_active', 'memo'
        ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user_id=request.user)

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # 新しいオブジェクトの場合のみ
            obj.user_id = request.user
        # UserProfileが存在しない場合は作成
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        # 編集または新規作成の場合
        if obj.is_active and not user_profile.lifted_account_number:
            # 他の is_active=True のデータの数を数える（自身を除く）
            active_count = Happymail.objects.filter(user_id=obj.user_id, is_active=True).exclude(pk=obj.pk).count()
            if active_count >= 8:
                messages.error(request, 'アクティブな Happymail キャラが　上限を超えました。')
                return  # データの保存をキャンセル

        super().save_model(request, obj, form, change)

    def response_add(self, request, obj, post_url_continue=None):
        # 成功メッセージを抑制し、リダイレクト
        messages.set_level(request, messages.WARNING)
        response = super().response_add(request, obj, post_url_continue)
        messages.set_level(request, messages.SUCCESS)
        return HttpResponseRedirect(reverse('admin:app_happymail_changelist'))

    def response_change(self, request, obj):
        # 成功メッセージを抑制し、リダイレクト
        messages.set_level(request, messages.WARNING)
        response = super().response_change(request, obj)
        messages.set_level(request, messages.SUCCESS)
        return HttpResponseRedirect(reverse('admin:app_happymail_changelist'))

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        # スーパーユーザーでない場合、idとuser_idを表示しない
        if not request.user.is_superuser:
            fields = [field for field in fields if field not in ('id', 'user_id')]
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        # print(777)
        # print(user_profile.check_mail_happymail)
        # if not user_profile.check_mail_happymail:
            # fields = [field for field in fields if field not in ('fst_message', )]
            # fields = [field for field in fields if field not in ('fst_message', 'second_message')]
        return fields

    def get_list_display(self, request):
        if request.user.is_superuser:   
            return ['user_id'] + self.list_display
        return self.list_display

admin.site.register(Happymail, HappymailAdmin)

class JmailAdmin(admin.ModelAdmin):
    list_display = ['name',  'login_id', 'is_active','memo']
    fields = [
        'user_id', 'name', 'login_id', 'password', 'post_title', 
        'post_contents', 'return_foot_message', 'fst_message', 'chara_image', 'conditions_message', 
        'is_active', 'memo'
        ]
    
    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        # スーパーユーザー以外は user_id フィールドを表示しない
        if not request.user.is_superuser:
            fields = [field for field in fields if field not in ('user_id',)]
        return fields
    
    def get_queryset(self, request):
        # スーパーユーザーは全データを表示
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # 一般ユーザーは自分のデータのみ表示
        return qs.filter(user_id=request.user)

    def save_model(self, request, obj, form, change):
        # 新規作成時に user_id を自動的に設定
        if not obj.pk:  # 新しいオブジェクトの場合のみ
            obj.user_id = request.user
        super().save_model(request, obj, form, change)

    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # スーパーユーザー以外は user_id を自動的に設定し、編集不可にする
        if db_field.name == 'user_id' and not request.user.is_superuser:
            kwargs['initial'] = request.user.id
            kwargs['disabled'] = True  # フィールドを編集不可に設定
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_list_display(self, request):
        # スーパーユーザーのみ user_id を表示
        if request.user.is_superuser:
            return ['user_id'] + self.list_display
        return self.list_display

    def get_list_display(self, request):
        # スーパーユーザーのみ user_id を表示
        if request.user.is_superuser:
            # return ['user_id'] + self.list_display
            return ['user_id'] + list(self.list_display) 
            
        return self.list_display
admin.site.register(Jmail, JmailAdmin)

class IkukuruAdmin(admin.ModelAdmin):
    list_display = ['name',  'login_mail_address', 'is_active','memo']
    fields = [
        'user_id', 'name', 'login_mail_address', 'password',  
        'fst_message',  'second_message', 'condition_message',
        'gmail_address', 'gmail_password',
        'is_active', 'memo',
        ]
    
    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        # スーパーユーザー以外は user_id フィールドを表示しない
        if not request.user.is_superuser:
            fields = [field for field in fields if field not in ('user_id',)]
        return fields
    
    def get_queryset(self, request):
        # スーパーユーザーは全データを表示
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # 一般ユーザーは自分のデータのみ表示
        return qs.filter(user_id=request.user)

    def save_model(self, request, obj, form, change):
        # 新規作成時に user_id を自動的に設定
        if not obj.pk:  # 新しいオブジェクトの場合のみ
            obj.user_id = request.user
        super().save_model(request, obj, form, change)

    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # スーパーユーザー以外は user_id を自動的に設定し、編集不可にする
        if db_field.name == 'user_id' and not request.user.is_superuser:
            kwargs['initial'] = request.user.id
            kwargs['disabled'] = True  # フィールドを編集不可に設定
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_list_display(self, request):
        # スーパーユーザーのみ user_id を表示
        if request.user.is_superuser:
            return ['user_id'] + self.list_display
        return self.list_display

    def get_list_display(self, request):
        # スーパーユーザーのみ user_id を表示
        if request.user.is_superuser:
            # return ['user_id'] + self.list_display
            return ['user_id'] + list(self.list_display) 
            
        return self.list_display
admin.site.register(Ikukuru, IkukuruAdmin)