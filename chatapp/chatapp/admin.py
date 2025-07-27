from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserProfile, ChatMessage

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'

class CustomUserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('id', 'username', 'first_name', 'email', 'get_image')

    def get_image(self, obj):
        if hasattr(obj, 'userprofile') and obj.userprofile.image:
            return obj.userprofile.image.url
        return ''
    get_image.allow_tags = True
    get_image.short_description = 'Profile Pic'

class AllMessagesInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    fields = ('from_user', 'to_user', 'message', 'created_at')
    readonly_fields = ('from_user', 'to_user', 'message', 'created_at')
    can_delete = False
    show_change_link = False

    def has_add_permission(self, request, obj=None):
        return False

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)  # Optional: if you want to manage profile separately
admin.site.register(ChatMessage)