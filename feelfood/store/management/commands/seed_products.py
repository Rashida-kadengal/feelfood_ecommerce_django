from django.core.management.base import BaseCommand
from store.models import Product
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Seed 100 products with random data and Lorem Flickr image URLs'

    def handle(self, *args, **options):
        fake = Faker()
        
        # List of Lorem Flickr image URLs
        image_urls = [
            f"https://loremflickr.com/400/300/product?lock={i}" for i in range(1, 101)
        ]


        for i in range(100):
            name = fake.catch_phrase()
            description = fake.paragraph(nb_sentences=3)
            price = round(random.uniform(10, 1000), 2)
            stock = random.randint(0, 100)
            image_url = image_urls[i]

            Product.objects.create(
                name=name,
                description=description,
                price=price,
                stock=stock,
                image_url=image_url,
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded 100 products'))