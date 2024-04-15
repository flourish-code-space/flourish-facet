import pandas as pd
from django.apps import apps as django_apps
from django.db.models import Subquery, OuterRef

from edc_base.utils import get_utcnow
from dateutil.relativedelta import relativedelta
from edc_constants.constants import YES
from django.db.models import Max, F, Min, Q, Value
from django.db.models.functions import Coalesce, Cast
from django.db.models import DateField


class EligibleFacetParticipantsMixin:
    child_hiv_rapid_test_model = 'flourish_child.childhivrapidtestcounseling'
    antenatal_enrollment_model = 'flourish_caregiver.antenatalenrollment'
    facet_screening_model = 'flourish_facet.facetsubjectscreening'
    facet_consent_model = 'flourish_facet.facetconsent'
    subject_consent_model = 'flourish_caregiver.subjectconsent'
    child_offstudy_model = 'flourish_prn.childoffstudy'
    caregiver_offstudy_model = 'flourish_prn.caregiveroffstudy'
    flourish_child_consent_model = 'flourish_caregiver.caregiverchildconsent'

    @property
    def subject_consent_cls(self):
        return django_apps.get_model(self.subject_consent_model)

    @property
    def antenatal_enrollment_cls(self):
        return django_apps.get_model(self.antenatal_enrollment_model)

    @property
    def flourish_child_consent_cls(self):
        return django_apps.get_model(self.flourish_child_consent_model)

    @property
    def facet_screening_cls(self):
        return django_apps.get_model(self.facet_screening_model)

    @property
    def facet_consent_cls(self):
        return django_apps.get_model(self.facet_consent_model)

    @property
    def child_hiv_rapid_test_cls(self):
        return django_apps.get_model(self.child_hiv_rapid_test_model)

    @property
    def child_offstudy_cls(self):
        return django_apps.get_model(self.child_offstudy_model)

    @property
    def caregiver_offstudy_cls(self):
        return django_apps.get_model(self.caregiver_offstudy_model)

    @property
    def child_offstudy_identifiers(self):
        identifiers = self.child_offstudy_cls.objects.values_list(
            'subject_identifier', flat=True)
        return identifiers


    @property
    def caregiver_offstudy_identifiers(self):
        identifiers = self.caregiver_offstudy_cls.objects.values_list(
            'subject_identifier', flat=True)
        return identifiers

    def eligible_participants(self, queryset):
        dates_before = (get_utcnow() - relativedelta(months=6, days=10)
                        ).date().isoformat()

        today = get_utcnow().date().isoformat()

        anc_subject_identifiers = self.antenatal_enrollment_cls.objects.exclude(
            child_subject_identifier__in=self.child_offstudy_identifiers).values_list(
            'child_subject_identifier', flat=True)


        subject_identifiers_dict = self.flourish_child_consent_cls.objects.filter(
            Q(child_dob__range=[dates_before, today]) | Q(
                child_dob__isnull=True),

            subject_identifier__in=anc_subject_identifiers,
            subject_consent__future_contact=YES
        ).values('subject_consent__subject_identifier', 'subject_identifier')

        subject_identifiers_df = pd.DataFrame(subject_identifiers_dict)

        facet_screened_identifiers = self.facet_screening_cls.objects.values_list(
            'subject_identifier', flat=True)


        consent_ids = []

        for _, row in subject_identifiers_df.iterrows():

            try:

                child_consent = self.flourish_child_consent_cls.objects.filter(
                    subject_identifier=row['subject_identifier'],
                    subject_consent__subject_identifier=row['subject_consent__subject_identifier']

                ).latest('version')

            except self.flourish_child_consent_cls.DoesNotExist:
                pass
            else:
                consent_ids.append(child_consent.subject_consent.id)

        return queryset.filter(Q(subject_identifier__in=facet_screened_identifiers) | Q(id__in=consent_ids,),
                               subject_identifier__startswith='B').annotate(
                                   _child_dob=Subquery(self.flourish_child_consent_cls.objects.filter(
                                       Q(child_dob__range=[dates_before, today]) | Q(
                                           child_dob__isnull=True),
                                       subject_consent=OuterRef('pk')).values('child_dob')[:1]),
            child_dob=Coalesce('_child_dob', Cast(get_utcnow().date(), DateField()))).exclude(
                subject_identifier__in=self.caregiver_offstudy_identifiers).order_by('child_dob')
