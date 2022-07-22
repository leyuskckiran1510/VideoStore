from django import forms
from video.models import Video
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'file']

    def save(self,user, commit=True):
        vid = Video.objects.create(
            title=self.cleaned_data['title'],
            description=self.cleaned_data['description'],
            file=self.cleaned_data['file'],
            author=user,
        )
        return vid


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise ValidationError('A user with that email already exists.')

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
