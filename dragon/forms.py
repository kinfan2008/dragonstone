from django import forms
from dragon.models import UserProfile,Experiment,ApplyRecord
from django.contrib.auth.models import User

Choice_education_demand = (('Undergraduate', 'Undergraduate'),
                            ('Master', 'Master'),
                            ('PHD', 'PHD'))
Choice_gender=(('Male', 'Male'),('Female', 'Female'))
Choice_language=(('English','English'),('Chinese','Chinese'),('Russian','Russian'),('French','French'),('Japanese','Japanese'),('Spanish','Spanish'),('Arabic','Arabic'),
                 ('Italian','Italian'),('Swedish','Swedish'),('Portuguese','Portuguese'),('Any','Any'))
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password','first_name','last_name')

class UserProfileForm(forms.ModelForm):
    age = forms.IntegerField( initial=18,required=True)
    gender = forms.TypedChoiceField( help_text="Please choose your gender Male or Female.",widget=forms.Select,
                                              choices=Choice_gender)
    educationLevel=forms.TypedChoiceField(widget=forms.Select,choices=Choice_education_demand)
    firstLanguage=forms.TypedChoiceField(widget=forms.Select,choices=Choice_language)
    class Meta:
     model = UserProfile
    fields = ('website','picture','age','gender','educationLevel','firstLanguage')

class ExperimentForm(forms.ModelForm):
    title = forms.CharField(max_length=128,help_text="Please enter the title of the experiment.")
    payment = forms.IntegerField(help_text="Please enter the payment of the experiment.")
    startTime=forms.DateField(help_text="Please enter the Start Time of the experiment.")
    endTime=forms.DateField(help_text="Please enter the End Time of the experiment.")
    educationDemand=forms.TypedChoiceField(help_text="Please choose the Education Demand of the experiment.",widget=forms.Select,
                                              choices=Choice_education_demand)
    maxPosition= forms.IntegerField(help_text="Please enter the Max Position of the Experiment.")
    description=forms.CharField(max_length=5000,widget=forms.Textarea, help_text="Please enter the detail description of the experiment.")
    language=forms.TypedChoiceField(widget=forms.Select,choices=Choice_language,help_text="Please choose the Language Demand of the experiment.")
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Experiment

        fields = ('title', 'payment', 'description','educationDemand','language','startTime','endTime','maxPosition')
class ApplyRecordForm(forms.ModelForm):
    class Meta:
        # Provide an association between the ModelForm and a model
        model = ApplyRecord

        fields = ('ApplyTime','isProcessed','isOffered','isAccepted','isValid')