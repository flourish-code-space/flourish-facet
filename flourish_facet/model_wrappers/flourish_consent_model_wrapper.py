from datetime import datetime
from edc_base import get_utcnow
from django.apps import apps as django_apps
from django.conf import settings
from django.forms import model_to_dict
from edc_model_wrapper import ModelWrapper
from edc_base.utils import age
from .facet_screening_model_wrapper import FacetScreeningModelWrapper
from .facet_consent_model_wrapper import FacetConsentModelWrapper
from .facet_mother_locator_model_wrapper import LocatorModelWrapper
from ..models import FacetSubjectScreening, FacetConsent
from .facet_contact_wrapper import FacetContactModelWrapper
from flourish_caregiver.models import CaregiverContact


class FlourishConsentModelWrapper(ModelWrapper):
    model = 'flourish_caregiver.subjectconsent'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'facet_flourish_consent_listboard_url')
    next_url_attrs = ['subject_identifier', ]
    facet_screening_model = 'flourish_facet.facetsubjectscreening'
    facet_consent_model = 'flourish_facet.facetconsent'
    flourish_consent_model = 'flourish_caregiver.subjectconsent'

    subject_locator_model = 'flourish_caregiver.caregiverlocator'

    @property
    def subject_locator_cls(self):
        return django_apps.get_model(self.subject_locator_model)

    @property
    def flourish_consent_cls(self):
        return django_apps.get_model(self.flourish_consent_model)

    @property
    def facet_screening_cls(self):
        return django_apps.get_model(self.facet_screening_model)

    @property
    def facet_consent_cls(self):
        return django_apps.get_model(self.facet_consent_model)

    @property
    def flourish_consent_obj(self):
        try:
            obj = self.flourish_consent_cls.objects.filter(
                subject_identifier=self.object.subject_identifier
            ).latest('consent_datetime')

        except self.flourish_consent_cls.DoesNotExist:
            pass
        else:
            return obj

    @property
    def facet_screening_obj(self):
        try:
            obj = self.facet_screening_cls.objects.filter(
                subject_identifier=self.object.subject_identifier
            ).latest('report_datetime')
        except self.facet_screening_cls.DoesNotExist:
            pass
        else:
            return obj

    @property
    def facet_consent_obj(self):
        try:
            obj = self.facet_consent_cls.objects.filter(
                subject_identifier=self.object.subject_identifier
            ).latest('report_datetime')
        except self.facet_consent_cls.DoesNotExist:
            pass
        else:
            return obj

    def facet_cosentents(self):
        return self.facet_consent_cls.objects.values_list(
            'suject_identifier', flat=True)

    @property
    def facet_screening_wrapper(self):

        facet_screening_obj = self.facet_screening_obj or FacetSubjectScreening(
            subject_identifier=self.object.subject_identifier
        )

        return FacetScreeningModelWrapper(model_obj=facet_screening_obj)

    @property
    def facet_child_age(self):
        # if the child dob is not filed
        child_dob = getattr(self.object, 'child_dob', None)

        age_in_months = 0

        if child_dob:

            age_timedelta = age(child_dob, get_utcnow().date())

            age_in_months = (age_timedelta.years * 12) + age_timedelta.months

        return age_in_months

    @property
    def locator_obj(self):
        try:
            obj = self.subject_locator_cls.objects.get(
                subject_identifier=self.flourish_consent_obj.subject_identifier)
        except self.subject_locator_cls.DoesNotExist:
            return None
        return obj

    @property
    def locator_wrapper(self):

        locator_obj = self.locator_obj or self.subject_locator_cls(
            subject_identifier=self.flourish_consent_obj.subject_identifier
        )

        return LocatorModelWrapper(model_obj=locator_obj)

    @property
    def facet_consent_wrapper(self):

        target_fields = ['subject_identifier',
                         'consent_datetime',
                         'first_name',
                         'last_name',
                         'initials',
                         'language',
                         'is_literate',
                         'witness_name',
                         'gender',
                         'gender_other',
                         'dob',
                         'is_dob_estimated',
                         'identity',
                         'identity_type',
                         'confirm_identity',
                         'consent_to_participate',
                         'child_consent', ]

        flourish_consent_dict = model_to_dict(instance=self.flourish_consent_obj,
                                              fields=target_fields)

        facet_consent_obj = self.facet_consent_obj or FacetConsent(
            **flourish_consent_dict
        )

        return FacetConsentModelWrapper(model_obj=facet_consent_obj)

    @property
    def contact_wrapper(self):
        contact_entry = CaregiverContact(
            subject_identifier=self.flourish_consent_obj.subject_identifier,
            study_name='facet')
        return FacetContactModelWrapper(model_obj=contact_entry)
