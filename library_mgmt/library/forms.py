from django import forms
from .models import Book, Loan, Member
from datetime import date, timedelta

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'copies_total']

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'email', 'member_type']

class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['member', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date', 'min': (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default due date to 14 days from today
        if not self.instance.pk:  # Only for new loans
            self.fields['due_date'].initial = date.today() + timedelta(days=14)
    
    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        if due_date and due_date <= date.today():
            raise forms.ValidationError('Due date must be after today.')
        return due_date
