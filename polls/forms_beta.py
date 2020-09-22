from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

Occupations = [('', '---------'),
               ('K-12 Student', 'K-12 Student'),
               ('Undergraduate/College Student', 'Undergraduate/College Student'),
               ('Graduate Student', 'Graduate Student'),
               ('Post-Graduate Student', 'Post-Graduate Student'),
               ('Not a Student', 'Not a Student'),
               ('Professor','Professor'),
               ('Researcher', 'Researcher')]

TF = [('Yes', 'Yes'), ('No', 'No')]

Affiliation = [('', '---------'), ('University', 'University'), ('Government Agency', 'Government Agency'),
               ('Industry', 'Industry'), ('None of the above', 'None of the above')]
TimesVisited = [('', '---------'), ('None', 'None'), ('1 to 3 times', '1 to 3 times'),
                ('More than 4 times', 'More than 4 times')]


class SignUpForm(UserCreationForm):
    # first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    # last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='This will be your username to enter IROS 2020 On-Demand. Enter a valid email address; an email will be sent there to confirm your sign-up.')
    occupation = forms.ChoiceField(label='Select your primary role', choices=Occupations, required=True)
    affiliation = forms.ChoiceField(label='Select your affiliation', choices=Affiliation, required=True)
    previous_attendance = forms.ChoiceField(label='How many times have you attended IROS and/or ICRA before?',
                                            choices=TimesVisited, required=True)
    primary = forms.ChoiceField(label='Is your primary field of study, work or interest in robotics?', choices=TF,
                                widget=forms.RadioSelect, required=True)
    member = forms.ChoiceField(label='Are you an IEEE and/or RAS Member?', choices=TF, widget=forms.RadioSelect,
                               required=True)
    password1 = None
    password2 = None

    class Meta:
        model = User
        # fields = ('email', 'first_name', 'last_name')
        fields = ('email',)


    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password('a')
        user.email = self.cleaned_data['email'].lower();
        user.username = user.email
        if commit:
            user.save()
        return user



