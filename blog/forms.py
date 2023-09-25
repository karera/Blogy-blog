from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . import models
from django.db.migrations.state import get_related_models_tuples
from django.utils.translation import gettext_lazy as _


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email','password1','password2']

    def save (self,commit =True):
        user = super(NewUserForm,self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit :
            user.save()
        return user

class BlogForm(forms.ModelForm):
     class Meta:
        model = models.Blog
        fields = ['title', 'content','image','categories','status']


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ('content','parent')
        
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        # self.fields['name'].widget.attrs = {'placeholder': 'Enter name','class':'form-control'}
        # self.fields['email'].widget.attrs = {'placeholder': 'Enter email', 'class':'form-control'}
        self.fields['content'].widget.attrs = {'placeholder': 'Comment here...', 'class':'form-control', 'rows':'5'}