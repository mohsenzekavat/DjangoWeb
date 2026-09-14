from django import forms
from django.contrib.auth.models import User

from .models import Comment, Post, User, Account


class TicketForm(forms.Form):
    SUBJECT_CHOICES = (
        ('SUGGESTIONS', 'Suggestions'),
        ('CRITICISM', 'Criticism'),
        ('REPORT', 'Report'),
    )
    message = forms.CharField(widget=forms.Textarea, required=True)
    name = forms.CharField(max_length=250, required=True)
    email = forms.EmailField()
    phone = forms.CharField(max_length=11, required=True)
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES)

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone:
            if not phone.isnumeric():
                raise forms.ValidationError('Please enter a valid phone number')
            else:
                return phone


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body')
        widgets = {
            'body': forms.TextInput(attrs={
                'placeholder': 'Your comment',
                'class': 'comment-body'
            }),
            'name': forms.TextInput(attrs={
                'placeholder': 'name',
                'class': 'name'
            })
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if name:
            if len(name) < 3:
                raise forms.ValidationError('Name must be at least 3 characters')
            else:
                return name


class SearchForm(forms.Form):
    query = forms.CharField()


class PostForm(forms.ModelForm):
    image1 = forms.ImageField(label='first images')
    image2 = forms.ImageField(label='second images')

    class Meta:
        model = Post
        fields = ['title', 'description', 'reading_time', 'category']


# class LoginForm(forms.Form):
#     username = forms.CharField(max_length=250, required=True)
#     password = forms.CharField(widget=forms.PasswordInput, max_length=250, required=True)
#
#     class Meta:
#         model = User
#         fields = ['username', 'password']


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(max_length=20, widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(max_length=20, widget=forms.PasswordInput, label='Repeat Password')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords must match')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class AccountEditForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['date_of_birth', 'bio', 'job', 'photo']
