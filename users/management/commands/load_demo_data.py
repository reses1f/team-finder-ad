from django.core.management.base import BaseCommand
import json
from projects.models import Project
from users.avatar import DEMO_AVATAR_FILES
from users.models import User
import os


class Command(BaseCommand):
    help = "Загружает тестовых пользователей и проекты для проверки Team Finder"

    def handle(self, *args, **options):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(current_dir, "demo_users.json")

        # Читаем данные из файла
        with open(json_path, "r", encoding="utf-8") as f:
            demo_users = json.load(f)


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
                
            # ЭТА СТРОКА ДОЛЖНА БЫТЬ ТУТ (с отступом 12 пробелов, вне блоков if/else)
            users.append(user)

            json_projects_path = os.path.join(current_dir, "demo_projects.json")
        with open(json_projects_path, "r", encoding="utf-8") as f:
            projects_data = json.load(f)

        for data in projects_data:
            owner_index = data.pop("owner_index")
            owner = users[owner_index]
            
            status_str = data.pop("status")
            status = Project.STATUS_OPEN if status_str == "open" else Project.STATUS_CLOSED

            project, created = Project.objects.get_or_create(
                name=data["name"],
                owner=owner,
                defaults={
                    "description": data["description"],
                    "status": status,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Создан проект: {project.name}"))
            else:
                self.stdout.write(f"Проект {project.name} уже существует")


      