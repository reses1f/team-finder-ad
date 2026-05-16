from django.core.management.base import BaseCommand

from users.avatar import DEMO_AVATAR_FILES
from users.models import User


class Command(BaseCommand):
    help = "Назначает иллюстрированные аватары как на team-finder.tech"

    def handle(self, *args, **options):
        for user in User.objects.all():
            if user.email in DEMO_AVATAR_FILES:
                user.assign_preset_avatar(DEMO_AVATAR_FILES[user.email])
            else:
                user.assign_preset_avatar()
            self.stdout.write(f"Обновлён аватар: {user.email}")
        self.stdout.write(self.style.SUCCESS("Готово."))
