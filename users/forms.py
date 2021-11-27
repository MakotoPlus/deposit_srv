from django import forms
from django.utils import timezone
from django.forms.fields import DateField  
from .models import User

#
# これ使うのかな?
#########################################
# ユーザ情報変更フォーム
#########################################
class UserUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            #field.widget.attrs['class'] = 'form-control-plaintext'
        #self.fields['username'].widget.attrs = 'form-control-plaintext'
        #self.fields['email'].widget.attrs = 'form-control-plaintext'

    class Meta:
        model = User
        #fields = ['username', 'full_name', 'email', 'tm_department',]
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username':forms.TextInput(attrs={'readonly':True}),
            'first_name':forms.TextInput(attrs={'readonly':True}),
            'last_name':forms.TextInput(attrs={'readonly':True}),
            'email':forms.TextInput(attrs={'readonly':True}),
        }
        '''
        'username':forms.TextInput(attrs={'readonly':True,'class':'form-control'}),
        'first_name':forms.TextInput(attrs={'readonly':True,'class':'form-control'}),
        'last_name':forms.TextInput(attrs={'readonly':True,'class':'form-control'}),
        'email':forms.TextInput(attrs={'readonly':True,'class':'form-control'}),
        '''
        '''
        'username':forms.TextInput(attrs={'readonly':True,'class':'form-control-plaintext'}),
        'first_name':forms.TextInput(attrs={'readonly':True,'class':'form-control-plaintext'}),
        'last_name':forms.TextInput(attrs={'readonly':True,'class':'form-control-plaintext'}),
        'email':forms.TextInput(attrs={'readonly':True,'class':'form-control-plaintext'}),
        '''

