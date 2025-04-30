from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from app.models import UserProfile

class Command(BaseCommand):
    help = 'Checks and updates the is_active status of users'

    def handle(self, *args, **kwargs):
        now = timezone.now().date()
        profiles = UserProfile.objects.filter(registration_subscribe_date__isnull=False)
        for profile in profiles:
            if profile.registration_subscribe_date + timedelta(days=30) < now:
                # self.stdout.write(f"{profile.user.username}は有効期限が切れました。{now}")
                profile.is_active = False
                profile.check_mail = False
                profile.save()

        self.stdout.write(self.style.SUCCESS('Successfully updated profiles'))