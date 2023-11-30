from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'author', 'price', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 8}),
        }
