from django.core.management.base import BaseCommand

from projects.models import Project
from users.avatar import DEMO_AVATAR_FILES
from users.models import User


class Command(BaseCommand):
    help = "Загружает тестовых пользователей и проекты для проверки Team Finder"

    def handle(self, *args, **options):
        demo_users = [
            {
                "email": "anna@example.com",
                "password": "demo12345",
                "name": "Анна",
                "surname": "Иванова",
                "phone": "+79001111111",
                "about": "Fullstack-разработчик, люблю open source.",
            },
            {
                "email": "boris@example.com",
                "password": "demo12345",
                "name": "Борис",
                "surname": "Петров",
                "phone": "+79002222222",
                "about": "Backend на Python и Django.",
            },
            {
                "email": "maria@example.com",
                "password": "demo12345",
                "name": "Мария",
                "surname": "Сидорова",
                "phone": "+79003333333",
                "about": "UI/UX и фронтенд.",
            },
        ]

        users = []
        for data in demo_users:
            user, created = User.objects.get_or_create(
                email=data["email"],
                defaults={
                    "name": data["name"],
                    "surname": data["surname"],
                    "phone": data["phone"],
                    "about": data["about"],
                },
            )
            if created:
                user.set_password(data["password"])
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Создан пользователь {user.email}"))
            else:
                self.stdout.write(f"Пользователь {user.email} уже существует")
            user.assign_preset_avatar(DEMO_AVATAR_FILES[data["email"]])
            users.append(user)

        projects_data = [
            {
                "owner": users[0],
                "name": "Платформа для поиска команды",
                "description": "Веб-сервис для студентов и разработчиков.",
                "status": Project.STATUS_OPEN,
            },
            {
                "owner": users[1],
                "name": "API для мобильного приложения",
                "description": "REST API на Django REST framework.",
                "status": Project.STATUS_OPEN,
            },
            {
                "owner": users[2],
                "name": "Редизайн лендинга",
                "description": "Обновление UI и адаптивной вёрстки.",
                "status": Project.STATUS_CLOSED,
            },
        ]

        for data in projects_data:
            owner = data.pop("owner")
            project, created = Project.objects.get_or_create(
                name=data["name"],
                owner=owner,
                defaults=data,
            )
            if created:
                project.participants.add(owner)
                self.stdout.write(self.style.SUCCESS(f"Создан проект «{project.name}»"))
            else:
                self.stdout.write(f"Проект «{project.name}» уже существует")

        if len(users) >= 2:
            users[1].favorites.add(Project.objects.filter(owner=users[0]).first())
        if len(users) >= 3 and Project.objects.filter(owner=users[1]).exists():
            users[2].favorites.add(Project.objects.filter(owner=users[1]).first())

        self.stdout.write(self.style.SUCCESS("Демо-данные загружены."))
