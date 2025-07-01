from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Book, Member, Loan, Fine
from .forms import BookForm, LoanForm, MemberForm
from datetime import date
from django.core.exceptions import ValidationError

def book_list(request):
    books = Book.objects.all()
    return render(request, 'library/book_list.html', {'books': books})

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.copies_available = book.copies_total
            book.save()
            messages.success(request, 'Book added successfully!')
            return redirect('book-list')
    else:
        form = BookForm()
    return render(request, 'library/book_form.html', {'form': form})

def delete_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        return redirect('book-list')
    return render(request, 'library/delete_book.html', {'book': book})

def member_list(request):
    members = Member.objects.all()
    return render(request, 'library/member_list.html', {'members': members})

def add_member(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Member added successfully!')
            return redirect('member-list')
    else:
        form = MemberForm()
    return render(request, 'library/member_form.html', {'form': form})

def delete_member(request, member_id):
    member = get_object_or_404(Member, pk=member_id)
    
    # Check if member has active loans
    active_loans = member.get_active_loans()
    if active_loans.exists():
        messages.error(request, f'Cannot delete {member.name}. They have {active_loans.count()} active loan(s). Please return all books first.')
        return redirect('member-list')
    
    if request.method == 'POST':
        member.delete()
        messages.success(request, f'Member {member.name} deleted successfully!')
        return redirect('member-list')
    
    return render(request, 'library/delete_member.html', {'member': member})

def borrow_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    
    if not book.is_available():
        messages.error(request, 'This book is not available for borrowing.')
        return redirect('book-list')
    
    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.book = book
            loan.loan_date = date.today()
            
            try:
                # Validate the loan before saving
                loan.full_clean()
                # Borrow the book
                if book.borrow_copy():
                    loan.save()
                    messages.success(request, f'Book "{book.title}" borrowed successfully by {loan.member.name}')
                    return redirect('book-list')
                else:
                    messages.error(request, 'Book is no longer available.')
            except ValidationError as e:
                for field, errors in e.message_dict.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
    else:
        form = LoanForm(initial={'book': book})
    
    return render(request, 'library/loan_form.html', {'form': form, 'book': book})

def return_book(request, loan_id):
    loan = get_object_or_404(Loan, pk=loan_id)
    
    if request.method == 'POST':
        fine_amount = loan.return_book()
        if fine_amount > 0:
            messages.warning(request, f'Book returned successfully. Fine of ₹{fine_amount} has been applied for overdue return.')
        else:
            messages.success(request, 'Book returned successfully!')
        return redirect('loan-list')
    
    return render(request, 'library/return_book.html', {'loan': loan})

def loan_list(request):
    loans = Loan.objects.all().order_by('-loan_date')
    return render(request, 'library/loan_list.html', {'loans': loans})

def fine_list(request):
    fines = Fine.objects.all()
    return render(request, 'library/fine_list.html', {'fines': fines})

def pay_fine(request, fine_id):
    fine = get_object_or_404(Fine, pk=fine_id)
    if request.method == 'POST':
        fine.mark_as_paid()
        messages.success(request, f'Fine of ₹{fine.amount} marked as paid.')
        return redirect('fine-list')
    return render(request, 'library/pay_fine.html', {'fine': fine})

