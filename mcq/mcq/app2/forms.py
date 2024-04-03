from django import forms
from app.models import *
from account.models import User
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class CategoriesForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = '__all__'

class QuestionSetsForm(forms.ModelForm):
    class Meta:
        model = QuestionSets
        fields = '__all__'
        
class SliderForm(forms.ModelForm):
    class Meta:
        model = Slider
        fields = '__all__'
        
        
from django.forms import inlineformset_factory

# class QuestionsForm(forms.ModelForm):
#     class Meta:
#         model = Questions
#         fields = '__all__'
#         widgets = {
#             'question': forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter Question'})
#         }

        
# class AnswerForm(forms.ModelForm):
#     class Meta:
#         model = Answer
#         fields = '__all__'
#         widgets = {
#             'answer': forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter Answer'})
#         }


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'

class QuestionsForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = ['group','marks','set_name', 'question', 'image', 'audio']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer', 'audio', 'image', 'correct']


AnswerFormSet = inlineformset_factory(
    Questions, 
    Answer, 
    form=AnswerForm, 
    max_num=4,  
)


from django.contrib.auth.hashers import make_password

class StudentRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields =['name','email','phone_No','password','avatar']
        exclude = ['is_user', 'is_admin', 'last_login']

    def __init__(self, *args, **kwargs):
        super(StudentRegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'password':
                self.fields[field_name].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': f'Enter your {field_name}', 'id': 'id_password'})


            if field_name == "avatar":
                self.fields[field_name].widget = forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'Enter image', 'onchange': 'showPreview(this);'})

            self.fields[field_name].widget.attrs['placeholder'] = f'Enter your {field_name}'
            
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            hashed_password = make_password(password)
            return hashed_password
        else:
            raise forms.ValidationError("Password field is required.")
            