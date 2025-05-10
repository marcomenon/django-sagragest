from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from sagragest.models import Event, CategoryTemplate, ProductTemplate, CategoryEvent, ProductEvent, Daytime, Order, OrderItem, OrderStatus
from django.utils import timezone
import random
from faker import Faker

class Command(BaseCommand):
    help = "Popola il database con dati di esempio per Sagragest."

    def handle(self, *args, **options):
        fake = Faker('it_IT')
        User = get_user_model()

        # 1. Gruppi
        parrocchia, _ = Group.objects.get_or_create(name="Parrocchia")
        ac, _ = Group.objects.get_or_create(name="Azione Cattolica")
        self.stdout.write(self.style.SUCCESS("Gruppi creati."))

        # 2. Utenti
        user1, _ = User.objects.get_or_create(username="n.rostellato", defaults={
            "email": "n.rostellato@example.com",
        })
        user1.set_password("Zeliel.87")
        user1.save()
        user1.groups.set([parrocchia])

        user2, _ = User.objects.get_or_create(username="d.rostellato", defaults={
            "email": "d.rostellato@example.com",
        })
        user2.set_password("Zeliel.87")
        user2.save()
        user2.groups.set([ac])
        self.stdout.write(self.style.SUCCESS("Utenti creati."))

        # 3. Eventi
        eventi = [
            ("Sagra san Rocco", parrocchia),
            ("Festa della Comunità", parrocchia),
            ("Panini AC", ac),
        ]
        eventi_objs = []
        for nome, gruppo in eventi:
            ev, _ = Event.objects.get_or_create(name=nome, year=2024, group=gruppo)
            eventi_objs.append(ev)
        self.stdout.write(self.style.SUCCESS("Eventi creati."))

        # 4. Categorie
        categorie = []
        for _ in range(6):
            nome = fake.unique.word().capitalize()
            cat, _ = CategoryTemplate.objects.get_or_create(name=nome, defaults={"description": fake.sentence()})
            categorie.append(cat)
        self.stdout.write(self.style.SUCCESS("Categorie create."))

        # 5. Prodotti per categoria
        prodotti = []
        for cat in categorie:
            for _ in range(6):
                nome = fake.unique.word().capitalize()
                prod, _ = ProductTemplate.objects.get_or_create(name=nome, defaults={"description": fake.sentence()})
                prodotti.append((cat, prod))
        self.stdout.write(self.style.SUCCESS("Prodotti creati."))

        # 6. CategoryEvent e ProductEvent
        for ev in eventi_objs:
            cat_events = []
            for cat in categorie:
                ce, _ = CategoryEvent.objects.get_or_create(event=ev, category=cat)
                cat_events.append(ce)
            for ce in cat_events:
                for cat, prod in prodotti:
                    if cat == ce.category:
                        price = round(random.uniform(2, 15), 2)
                        ProductEvent.objects.get_or_create(event=ev, product=prod, category=ce, defaults={"price": price})
        self.stdout.write(self.style.SUCCESS("CategoryEvent e ProductEvent creati."))

        # 7. Daytime per ogni evento
        daytimes = []
        for ev in eventi_objs:
            start = timezone.now().replace(hour=18, minute=0, second=0, microsecond=0)
            dt, _ = Daytime.objects.get_or_create(event=ev, start=start)
            daytimes.append(dt)
        self.stdout.write(self.style.SUCCESS("Daytime creati."))

        # 8. Ordini e OrderItem
        for _ in range(15):
            dt = random.choice(daytimes)
            ev = dt.event
            user = random.choice([user1, user2])
            number = Order.get_next_number_for_daytime(dt)
            ordine = Order.objects.create(
                number=number,
                daytime=dt,
                event=ev,
                status=random.choice([OrderStatus.ORDERED, OrderStatus.IN_PREPARATION, OrderStatus.READY]),
                created_by=user,
                total=0.0
            )
            # OrderItems
            items = []
            for _ in range(5):
                # Scegli un ProductEvent valido per l'evento
                pe = ProductEvent.objects.filter(event=ev).order_by('?').first()
                if not pe:
                    continue
                qty = random.randint(1, 4)
                item = OrderItem.objects.create(
                    order=ordine,
                    product_event=pe,
                    quantity=qty,
                    price_at_order_time=pe.price
                )
                items.append(item)
            # Calcola totale ordine
            totale = sum(i.total_price for i in items if i.total_price)
            ordine.total = totale
            ordine.save()
        self.stdout.write(self.style.SUCCESS("Ordini e OrderItem creati."))
        self.stdout.write(self.style.SUCCESS("Database popolato con dati di esempio!"))
