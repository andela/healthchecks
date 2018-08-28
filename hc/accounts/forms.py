from datetime import timedelta as td
from django import forms


class LowercaseEmailField(forms.EmailField):

    def clean(self, value):
        value = super(LowercaseEmailField, self).clean(value)
        return value.lower()


class EmailPasswordForm(forms.Form):
    email = LowercaseEmailField()
    password = forms.CharField(required=False)


class ReportSettingsForm(forms.Form):
    reports_allowed = forms.BooleanField(required=False)
    report_period = forms.CharField(required=False)

    def clean_report_period(self):
        report_frequency = self.cleaned_data["report_period"]
        submitted_frequency = td()

        if report_frequency in ("Daily","Weekly","Monthly"):
            switcher = {
                'Daily':td(days=1),
                'Weekly':td(days=7),
                'Monthly':td(days=30)
            }
            submitted_frequency = switcher[report_frequency]
        
        return submitted_frequency


class SetPasswordForm(forms.Form):
    password = forms.CharField()


class InviteTeamMemberForm(forms.Form):
    email = LowercaseEmailField()


class RemoveTeamMemberForm(forms.Form):
    email = LowercaseEmailField()


class TeamNameForm(forms.Form):
    team_name = forms.CharField(max_length=200, required=True)
