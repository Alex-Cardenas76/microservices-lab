from django.core.management.base import BaseCommand
from django.utils import timezone
from categories.models import Category
from authors.models import Author
from posts.models import Post
import random

class Command(BaseCommand):
    help = "Crea datos de ejemplo: categorías, autores y posts"

    def handle(self, *args, **options):
        self.stdout.write("Seeding Blog...")

        cats = [
            "Backend", "Frontend", "DevOps", "Datos", "Seguridad",
            "Arquitectura", "Testing"
        ]
        categories = []
        for name in cats[:5]:
            c, _ = Category.objects.get_or_create(name=name, defaults={"is_active": True})
            categories.append(c)

        authors_data = [
            ("Ada Lovelace", "ada@example.com"),
            ("Alan Turing", "alan@example.com"),
            ("Grace Hopper", "grace@example.com"),
        ]
        authors = []
        for dn, em in authors_data:
            a, _ = Author.objects.get_or_create(display_name=dn, email=em)
            authors.append(a)

        statuses = ["published", "draft"]
        created = 0
        for i in range(30):
            title = f"Post #{i+1} sobre {random.choice(['Django','DRF','Redis','Docker','PostgreSQL'])}"
            body = "Contenido de ejemplo " * random.randint(20, 60)
            Post.objects.get_or_create(
                title=title,
                defaults={
                    "body": body,
                    "author": random.choice(authors),
                    "category": random.choice(categories),
                    "status": random.choice(statuses),
                    "published_at": timezone.now(),
                    "views": random.randint(0, 100),
                }
            )
            created += 1

        self.stdout.write(self.style.SUCCESS(f"Seed listo. Posts creados/asegurados: {created}"))
