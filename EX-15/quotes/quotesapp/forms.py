from django.forms import ModelForm, CharField, TextInput, DateField, DateInput, Textarea, ModelChoiceField
from .models import Authors, Quotes, Tags


class MyModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        print(obj)
        return obj.fullname

class AuthorForm(ModelForm):
    fullname = CharField(min_length=3, max_length=150, required=True, widget=TextInput)
    born_date = DateField(required=True, widget=DateInput(attrs={'type': 'date', 'format': "%Y-%m-%d"}))
    born_location = CharField(max_length=150, required=False, widget=TextInput)
    description = CharField(max_length=5000, required=False, widget=Textarea)

    class Meta:
        model = Authors
        fields = ['fullname', 'born_date', 'born_location', 'description']


class TagForm(ModelForm):
    name = CharField(min_length=1, max_length=50, required=True, widget=TextInput)

    class Meta:
        model = Tags
        fields = ['name']


class QuoteForm(ModelForm):
    quote = CharField(max_length=5000, required=True, widget=Textarea)
    author = MyModelChoiceField(queryset=Authors.objects.all().order_by('fullname'))

    class Meta:
        model = Quotes
        fields = ['quote', 'author']
        exclude = ['tags']
