from django.forms import Form, ModelForm, BooleanField, CharField, ValidationError
from .models import Report, user_reporting_categories, other_reporting_categories, reportable_types
from . import utils as ReportUtil

class ReportForm(ModelForm):
    report_type = CharField(required=True)

    class Meta:
        model = Report
        fields = ('reportable_id', 'report_type', 'category', 'message')
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(ReportForm, self).__init__(*args, **kwargs)
    
    def clean(self):
        report_type = self.cleaned_data.get('report_type', None)
        category = self.cleaned_data.get('category', None)
        if report_type not in reportable_types:
            raise ValidationError('Provide valid reportable type.')
        categories = user_reporting_categories if report_type == "user" else other_reporting_categories
        if category not in categories:
            raise ValidationError('Provide valid category.')

    def save(self, commit=True):
        reportable_id = self.cleaned_data.get('reportable_id')
        report_type = self.cleaned_data.get('report_type')
        category = self.cleaned_data.get('category')
        message = self.cleaned_data.get('message')
        reportable = ReportUtil.get_reportable(reportable_id, report_type)
        if reportable == self.request.user:
            raise Exception("You can't report yourself")
        report = Report.objects.create(user=self.request.user, category=category, message=message, reportable=reportable)
        return report
            
