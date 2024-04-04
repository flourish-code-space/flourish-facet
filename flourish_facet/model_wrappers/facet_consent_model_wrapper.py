
from django.apps import apps as django_apps
from django.conf import settings
from edc_model_wrapper import ModelWrapper
from .qualitative_interview_scheduling_model_wrapper_mixin import QualitativeInterviewSchedulingModelWrapperMixin
from .qualitative_interview_audio_upload_model_wrapper_mixin import QualitativeInterviewAudioUploadModelWrapperMixin
from .qualitative_interview_trancription_translation_model_wrapper_mixin import QualitativeInterviewTranscriptionAndTranslationModelWrapperMixin
from .facet_contact_wrapper_mixin import FacetContactModelWrapperMixin

class FacetConsentModelWrapper(QualitativeInterviewSchedulingModelWrapperMixin,
                               QualitativeInterviewAudioUploadModelWrapperMixin,
                               QualitativeInterviewTranscriptionAndTranslationModelWrapperMixin,
                               FacetContactModelWrapperMixin,
                               ModelWrapper):
    model = 'flourish_facet.facetconsent'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'facet_flourish_consent_listboard_url')
    next_url_attrs = ['subject_identifier',]
    querystring_attrs = ['subject_identifier', 'first_name',
                         'last_name', 'initials', 'language',
                         'is_literate', 'witness_name', 'gender',
                         'gender_other', 'dob', 'is_dob_estimated',
                         'identity', 'identity_type', 'confirm_identity',
                         'consent_to_participate', 'child_consent',]

    focus_group_model = 'flourish_facet.focusgroupinterviewaudiouploads'

    @property
    def focus_group_cls(self):
        return django_apps.get_model(self.focus_group_model)

    @property
    def focus_group_obj(self):
        try:
            obj = self.focus_group_cls.objects.get(
                paticipant_ids__name=self.object.subject_identifier
            )
        except self.focus_group_cls.DoesNotExist:
            pass
        else:
            return obj

    @property
    def in_focus_group(self):
        return bool(self.focus_group_obj)
