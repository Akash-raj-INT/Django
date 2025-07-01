from django.db import models
from datetime import date
from django.core.exceptions import ValidationError

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    copies_total = models.IntegerField(default=1)
    copies_available = models.IntegerField(default=1)

    def __str__(self):
        return self.title
    
    def is_available(self):
        return self.copies_available > 0
    
    def borrow_copy(self):
        if self.copies_available > 0:
            self.copies_available -= 1
            self.save()
            return True
        return False
    
    def return_copy(self):
        if self.copies_available < self.copies_total:
            self.copies_available += 1
            self.save()
            return True
        return False

class Member(models.Model):
    MEMBER_TYPE_CHOICES = [
        ('Student', 'Student'),
        ('Teacher', 'Teacher'),
    ]
    
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    member_type = models.CharField(max_length=10, choices=MEMBER_TYPE_CHOICES, default='Student')

    def __str__(self):
        return f"{self.name} ({self.get_member_type_display()})"
    
    def get_active_loans(self):
        return self.loan_set.filter(status='borrowed')

class Loan(models.Model):
    STATUS_CHOICES = [
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned')
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    loan_date = models.DateField(default=date.today)
    due_date = models.DateField()
    return_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='borrowed')

    def __str__(self):
        return f"{self.book.title} borrowed by {self.member.name}"
    
    def clean(self):
        super().clean()
        if self.due_date and self.loan_date and self.due_date <= self.loan_date:
            raise ValidationError('Due date must be after the loan date.')
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    def calculate_fine(self):
        if self.return_date and self.return_date > self.due_date:
            overdue_days = (self.return_date - self.due_date).days
            return overdue_days * 5
        return 0
    
    def return_book(self):
        self.return_date = date.today()
        self.status = 'returned'
        self.save()
        
        
        self.book.return_copy()
        
        
        fine_amount = self.calculate_fine()
        if fine_amount > 0:
            Fine.objects.create(loan=self, amount=fine_amount)
        
        return fine_amount

class Fine(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    amount = models.FloatField()
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Fine for {self.loan} - ₹{self.amount}"
    
    def mark_as_paid(self):
        self.paid = True
        self.save()

