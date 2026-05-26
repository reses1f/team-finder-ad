from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .constants import USER_NAME_MAX_LENGTH


from users.avatar import (
    DEMO_AVATAR_FILES,
    generate_avatar_file,
    load_preset_avatar_file,
    preset_filename_for_name,
)
from users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=USER_NAME_MAX_LENGTH)
    surname = models.CharField(max_length=USER_NAME_MAX_LENGTH)
    avatar = models.ImageField(upload_to="avatars/")
    phone = models.CharField(max_length=12)
    github_url = models.URLField(blank=True)
    about = models.TextField(max_length=256, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    favorites = models.ManyToManyField(
        "projects.Project",
        related_name="interested_users",
        blank=True,
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname"]

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.name} {self.surname}"

    def _save_avatar_file(self, avatar_file):
        if self.avatar:
            self.avatar.delete(save=False)
        self.avatar.save(avatar_file.name, avatar_file, save=False)
        self.save(update_fields=["avatar"])

    def assign_preset_avatar(self, filename: str | None = None):
        if filename is None:
            filename = preset_filename_for_name(self.name)
        self._save_avatar_file(load_preset_avatar_file(filename))

    def regenerate_avatar(self, use_preset: bool = False):
        if use_preset or self.email in DEMO_AVATAR_FILES:
            filename = DEMO_AVATAR_FILES.get(self.email) or preset_filename_for_name(
                self.name
            )
            self.assign_preset_avatar(filename)
            return
        self._save_avatar_file(generate_avatar_file(self.name))

        class Meta:
         ordering = ["-id"]

    def __str__(self):
        return f"{self.name} {self.surname}"

    # === ПЕРЕНЕСИТЕ МЕТОД SAVE СЮДА ===
    def save(self, *args, **kwargs):
        if self.pk is None and not self.phone:
            self.phone = "80000000000"
        if self.pk is None and not self.avatar:
            avatar_file = generate_avatar_file(self.name)
            self.avatar.save(avatar_file.name, avatar_file, save=False)
        super().save(*args, **kwargs)


    def _save_avatar_file(self, avatar_file):
        if self.avatar:
            self.avatar.delete(save=False)
        self.avatar.save(avatar_file.name, avatar_file, save=False)
        self.save(update_fields=["avatar"])

    def assign_preset_avatar(self, filename: str | None = None):
        if filename is None:
            filename = preset_filename_for_name(self.name)
        self._save_avatar_file(load_preset_avatar_file(filename))

    def regenerate_avatar(self, use_preset: bool = False):
        if use_preset or self.email in DEMO_AVATAR_FILES:
            filename = DEMO_AVATAR_FILES.get(self.email) or preset_filename_for_name(
                self.name
            )
            self.assign_preset_avatar(filename)
            return
        self._save_avatar_file(generate_avatar_file(self.name))
