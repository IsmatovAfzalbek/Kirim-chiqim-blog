from django.core.management.base import BaseCommand
from django.utils import timezone
from dateutil.relativedelta import relativedelta


from apps.app_transactions.models import Transaction, RecurringTransaction
from apps.app_currencies.models import ExchangeRate





class Command(BaseCommand):
    help = "Takrorlanuvchi tranzaksiyalarni qayta ishlash"

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        recurring_list = RecurringTransaction.objects.select_related(
            'user', 'account', 'category', 'currency'
        ).filter(is_active=True, next_run_date__lte=today)

        count = 0

        for recurring in recurring_list:
            try:
                exchange_rate = ExchangeRate.objects.get(
                    currency=recurring.currency,
                    date=today
                )
                amount_uzs = recurring.amount * exchange_rate.rate_uzs
            except ExchangeRate.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(
                        f"{recurring.currency.code} uchun {today} sanasida kurs topilmadi. O'tkazib yuborildi."
                    )
                )
                continue

            Transaction.objects.create(
                user=recurring.user,
                account=recurring.account,
                category=recurring.category,
                transaction_type=recurring.transaction_type,
                amount=recurring.amount,
                currency=recurring.currency,
                amount_uzs=amount_uzs,
                description=f"Avtomatik: {recurring.title}",
                date=today,
            )

            if recurring.frequency == 'daily':
                recurring.next_run_date = today + relativedelta(days=1)
            elif recurring.frequency == 'weekly':
                recurring.next_run_date = today + relativedelta(weeks=1)
            elif recurring.frequency == 'monthly':
                recurring.next_run_date = today + relativedelta(months=1)
            elif recurring.frequency == 'yearly':
                recurring.next_run_date = today + relativedelta(years=1)

            if recurring.end_date and recurring.next_run_date > recurring.end_date:
                recurring.is_active = False

            recurring.save()
            count += 1
        self.stdout.write(self.style.SUCCESS(f"{count} ta tranzaksiya avtomatik yaratildi."))