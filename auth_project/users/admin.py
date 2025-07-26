from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_approved')
    actions = ['approve_users']

    def approve_users(self, request, queryset):
        for user in queryset:
            if not user.is_approved:
                user.is_approved = True
                user.save()
                user.email_user(
                     subject="Account Approved",
                    message=f"Your account is now approved. You may log in. Code: {user.registration_code}",
                    from_email="no-reply@yourapp.com"
                )
    approve_users.short_description = "Approve selected users"