from django.contrib import admin
from ...models import FocusGroupInterviewTranscriptionAndTranslation
from ...admin_site import flourish_facet_admin
from ...forms import FocusGroupInterviewTranscriptionAndTranslationForm
from edc_model_admin import audit_fieldset_tuple
from ..modeladmin_mixins import ModelAdminMixin


@admin.register(FocusGroupInterviewTranscriptionAndTranslation, site=flourish_facet_admin)
class FocusGroupInterviewTranscriptionAndTranslationAdmin(ModelAdminMixin, admin.ModelAdmin):
    form = FocusGroupInterviewTranscriptionAndTranslationForm

    fieldsets = (
        (None, {
            'fields': [
                'group_identifier',
                'report_datetime',
                'transcription_date',
                'facet_member_transcription',
                'transcription_duration',
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {
        'facet_member_transcription': admin.VERTICAL,
        'transcription_duration': admin.VERTICAL,
    }
