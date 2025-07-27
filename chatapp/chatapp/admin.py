from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserProfile

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

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)  # Optional: if you want to manage profile separately
