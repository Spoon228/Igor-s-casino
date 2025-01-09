from django import forms

class AddPointsForm(forms.Form):
    points = forms.IntegerField(label='Add Points', min_value=1)

class RemovePointsForm(forms.Form):
    points = forms.IntegerField(label='Remove Points', min_value=1)
