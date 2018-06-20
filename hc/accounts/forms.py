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
    report_period = forms.IntegerField(min_value=1, max_value=30, required=False)
    
    def clean_report_period(self):
        report_period = self.cleaned_data["report_period"]

        if not report_period:
            return 30

        if report_period not in (1, 7, 30):
            raise forms.ValidationError("Bad report_period: %d" % report_period)

        return report_period


class SetPasswordForm(forms.Form):
    password = forms.CharField()


class InviteTeamMemberForm(forms.Form):
    email = LowercaseEmailField()


class RemoveTeamMemberForm(forms.Form):
    email = LowercaseEmailField()


class TeamNameForm(forms.Form):
    team_name = forms.CharField(max_length=200, required=True)
