from django import forms

class UnifiedSearchForm(forms.Form):
    SEARCH_FIELDS = [
        ('emp_number', 'Employee Number'),
        ('alias', 'Alias'),
        ('region', 'Region'),
        ('email', 'Email'),
        ('date_joined', 'Date Joined'),
    ]

    field = forms.ChoiceField(choices=SEARCH_FIELDS, label='Search Field')
    query = forms.CharField(max_length=100, label='Search Query', required=True)
