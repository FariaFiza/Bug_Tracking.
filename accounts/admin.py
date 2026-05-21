from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'availability', 'is_approved', 'avg_rating', 'date_joined']
    list_filter = ['role', 'is_approved', 'availability']
    search_fields = ['username', 'email']
    fieldsets = UserAdmin.fieldsets + (
        ('BugHive Info', {
            'fields': ('role', 'bio', 'skills', 'availability', 'avatar_color', 'is_approved', 'total_rating',
                       'rating_count')}),
    )
    actions = ['ban_users', 'approve_users']

    def ban_users(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, "Selected users have been banned")

    # short_description ফাংশনের বাইরে, ক্লাসের লেভেলে থাকবে
    ban_users.short_description = "Ban selected users"

    def approve_users(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, "Selected users have been approved")

    # স্পেসিং বা ইন্ডেন্টেশন ঠিক করা হয়েছে
    approve_users.short_description = "Approve selected users"