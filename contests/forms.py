from django import forms
from .models import *


class UploadDataTrain(forms.Form):
    # title = forms.CharField(max_length=50)
    file = forms.FileField()


class ExerciseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # print('args', args.index((1,)))
        # print('kwargs', kwargs)
        self.file = kwargs.pop('file', None)

        # print("save---------", self.file)
        super().__init__(*args, **kwargs)

    # (
    #     < QueryDict: {'csrfmiddlewaretoken':['OSpRhKctmnchcdnNAqXSxRPIHvzqar4s1XWv2LwSGNzphJRqrm3qtxoasb3f5rhK'], 'submit':['Submit']} >,
    #          < MultiValueDict: {'file':[< InMemoryUploadedFile: a.py (text / x-python) >]} > )
    def save(self, commit=True):
        comment = super().save(commit=False)
        comment.file = self.file
        print("save---------", self.file)
        comment.save()

    class Meta:
        model = Exercise
        fields = ['file', ]
        widgets = {
            'parameters': forms.ClearableFileInput(attrs={'multiple':True}),
        }



class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        self.content = kwargs.pop('content', None)
        self.Exercise_post_connected = kwargs.pop('Exercise_post_connected', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        comment = super().save(commit=False)
        comment.author = self.author
        comment.content = self.content
        comment.Exercise_post_connected = self.Exercise_post_connected
        comment.save()

    class Meta:
        model = ExerciseComment
        fields = ['content']
        widgets = {
            'parameters': forms.Textarea(attrs={'cols': 30, 'rows': 9}),
        }


class CreateContestForm(forms.ModelForm):
    class Meta:
        model = Contest
        fields = ('name', 'contest_type', 'start', 'end', 'description', 'participant')
        widget = {
            # 'name': forms.TextInput(attrs={'size': 30}),
            #     # 'contest_type': forms.TextInput(attrs={'class': 'contest_type'}),
            #     # 'start': forms.DateTimeField(),
            #     # 'length': forms.TimeField(),
            #     # 'description': forms.Textarea(attrs={'class': 'description'}),
            #     # 'participant': forms.NumberInput(attrs={'class': 'participant'}),
            #
                # 'name': forms.TextInput(attrs={'class': 'name', 'width': '300px'}),
            #     'contest_type': forms.CharField(),
            #     'start': forms.DateTimeField(),
            #     'length': forms.CharField(),
            #     'description': forms.Textarea(attrs={'class': 'description'}),
            #     'participant': forms.NumberInput(),
        }