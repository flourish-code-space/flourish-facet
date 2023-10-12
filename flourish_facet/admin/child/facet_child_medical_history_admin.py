from django.contrib import admin
from edc_fieldsets.fieldlist import Insert
from edc_fieldsets.fieldsets_modeladmin_mixin import FormLabel
from edc_model_admin import audit_fieldset_tuple

from ...admin_site import flourish_facet_admin
from ...forms import FacetChildMedicalHistoryForm
from ...models import FacetChildMedicalHistory
from ..modeladmin_mixins import CrfModelAdminMixin


@admin.register(FacetChildMedicalHistory, site=flourish_facet_admin)
class FacetChildMedicalHistoryAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = FacetChildMedicalHistoryForm

    list_display = (
        'facet_visit', 'chronic_since')
    list_filter = ('chronic_since',)

    fieldsets = (
        (None, {
            'fields': [
                'facet_visit',
                'report_datetime',
                'chronic_since',
                'child_chronic',
                'child_chronic_other',
                'current_illness_child',
                'current_symptoms_child',
                'current_symptoms_child_other',
                'symptoms_start_date_child',
                'clinic_visit_child',
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'chronic_since': admin.VERTICAL,
                    'med_history_changed': admin.VERTICAL,
                    'current_illness_child': admin.VERTICAL,
                    'current_symptoms_child': admin.VERTICAL,
                    'clinic_visit_child': admin.VERTICAL}

    filter_horizontal = ('child_chronic',)

    custom_form_labels = [
        FormLabel(
            field='med_history_changed',
            label=('Since the last scheduled visit in {previous}, has any of '
                   'your medical history changed?'),
            previous_appointment=True)
        ]

    quartely_schedules = ['child_a_sec_qt_schedule1', 'child_a_quart_schedule1',
                          'child_b_sec_qt_schedule1', 'child_b_quart_schedule1',
                          'child_c_sec_qt_schedule1', 'child_c_quart_schedule1',
                          'child_pool_schedule1', 'child_a_fu_schedule1',
                          'child_b_fu_schedule1', 'child_c_fu_schedule1',
                          'child_a_fu_qt_schedule1', 'child_b_fu_qt_schedule1',
                          'child_c_fu_qt_schedule1']

    conditional_fieldlists = {}
    for schedule in quartely_schedules:
        conditional_fieldlists.update(
            {schedule: Insert('med_history_changed', after='report_datetime')})

    def get_form(self, request, obj=None, *args, **kwargs):
        form = super().get_form(request, *args, **kwargs)
        form.previous_instance = self.get_previous_instance(request)
        return form