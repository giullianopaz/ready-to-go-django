import os

from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

from apps.accounts.models import User


class Command(BaseCommand):
    help = "Seed database with default groups, permissions, and default superuser."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding database..."))

        # 1. Ensure Groups exist
        admin_group, _ = Group.objects.get_or_create(name="Admin")
        standard_group, _ = Group.objects.get_or_create(name="Standard User")
        self.stdout.write(self.style.SUCCESS("  ✔ Groups verified (Admin, Standard User)"))

        # 2. Assign all permissions to Admin group
        all_perms = Permission.objects.all()
        admin_group.permissions.set(all_perms)
        self.stdout.write(
            self.style.SUCCESS(f"  ✔ Admin group granted {all_perms.count()} permissions")
        )

        # 3. Create default superuser if none exists
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "admin123")

        if not User.objects.filter(is_superuser=True).exists():
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                first_name="Admin",
                last_name="User",
            )
            user.groups.add(admin_group)
            self.stdout.write(
                self.style.SUCCESS(
                    f"  ✔ Created default superuser: username='{username}', email='{email}', password='{password}'"
                )
            )
        else:
            self.stdout.write(
                self.style.NOTICE("  ℹ Superuser already exists — skipping creation.")
            )

        self.stdout.write(self.style.SUCCESS("Seeding complete!"))
