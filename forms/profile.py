from django.forms import ModelForm, ChoiceField
from jam.models.profile import Profile


class ProfileForm(ModelForm):

    class Meta:
        model = Profile
        fields = ['theme']
