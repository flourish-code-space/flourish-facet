from django.apps import apps as django_apps
from django.db.models import Q
from django.views.generic import TemplateView
from edc_constants.constants import POS, NEG, IND
from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin
from edc_appointment.constants import COMPLETE_APPT, IN_PROGRESS_APPT, NEW_APPT, CANCELLED_APPT
from ..views.eligible_facet_participants_mixin import EligibleFacetParticipantsMixin
from flourish_caregiver.helper_classes import MaternalStatusHelper
from ..models import Appointment


class HomeView(EdcBaseViewMixin, NavbarViewMixin, TemplateView, EligibleFacetParticipantsMixin):
    template_name = 'flourish_facet/home.html'
    navbar_name = 'flourish_facet'
    navbar_selected_item = 'home'

    facet_consent_model = 'flourish_facet.facetconsent'
    flourish_consent_model = 'flourish_caregiver.subjectconsent'
    facet_screening_model = 'flourish_facet.facetsubjectscreening'
    focus_group_model = 'flourish_facet.focusgroupinterviewaudiouploads'
    facet_appointment_model = 'flourish_facet.Appointment'
    antenatal_enrollment_model = 'flourish_caregiver.antenatalenrollment'
    flourish_child_consent_model = 'flourish_caregiver.caregiverchildconsent'

    @property
    def flourish_consent_cls(self):
        return django_apps.get_model(self.flourish_consent_model)

    @property
    def facet_subject_screening_cls(self):
        return django_apps.get_model(self.facet_screening_model)

    @property
    def facet_consent_cls(self):
        return django_apps.get_model(self.facet_consent_model)

    @property
    def facet_appointment_cls(self):
        return django_apps.get_model(self.facet_appointment_model)

    @property
    def facet_focus_group_cls(self):
        return django_apps.get_model(self.focus_group_model)

    @property
    def screened_hiv_statistics(self):
        statistics = dict()

        consents = self.facet_screening_cls.objects.all()

        positive_mothers = 0
        negative_mothers = 0
        ind_mothers = 0

        statistics.update(
            positive_mothers=positive_mothers,
            negative_mothers=negative_mothers,
            ind_mothers=ind_mothers
        )

        for consent in consents:
            helper = MaternalStatusHelper(
                subject_identifier=consent.subject_identifier)

            if helper.hiv_status == POS:
                positive_mothers += 1

            if helper.hiv_status == NEG:
                negative_mothers += 1

            if helper.hiv_status == IND:
                ind_mothers += 1

        statistics.update(
            positive_mothers=positive_mothers,
            negative_mothers=negative_mothers,
            ind_mothers=ind_mothers

        )
        return statistics

    @property
    def consented_hiv_statistics(self):
        statistics = dict()

        consents = self.facet_consent_cls.objects.all()

        positive_mothers = 0
        negative_mothers = 0
        ind_mothers = 0

        statistics.update(
            positive_mothers=positive_mothers,
            negative_mothers=negative_mothers,
            ind_mothers=ind_mothers
        )

        for consent in consents:
            helper = MaternalStatusHelper(
                subject_identifier=consent.subject_identifier)

            if helper.hiv_status == POS:
                positive_mothers += 1

            if helper.hiv_status == NEG:
                negative_mothers += 1

            if helper.hiv_status == IND:
                ind_mothers += 1

        statistics.update(
            positive_mothers=positive_mothers,
            negative_mothers=negative_mothers,
            ind_mothers=ind_mothers
        )

        return statistics

    @property
    def appointment_statistics(self):

        completed_appts = Appointment.objects.filter(
            appt_status=COMPLETE_APPT
        ).count()

        incompleted_appts = Appointment.objects.filter(
            appt_status=IN_PROGRESS_APPT
        ).count()

        new_appts = Appointment.objects.filter(
            appt_status=NEW_APPT
        ).count()

        cancelled_appts = Appointment.objects.filter(
            appt_status=CANCELLED_APPT
        ).count()

        return dict(
            completed_appts=completed_appts,
            incompleted_appts=incompleted_appts,
            new_appts=new_appts,
            cancelled_appts=cancelled_appts
        )

    def get_hiv_statistics(self, appt_status):
        """ Get hiv status based on the appointments status """
        statistics = dict()
        pos = 0
        neg = 0
        ind = 0

        appt_ids = Appointment.objects.filter(
            appt_status=appt_status,
            visit_code_sequence=0,
        ).values_list('subject_identifier', flat=True).distinct()

        for appt_id in appt_ids:
            helper = MaternalStatusHelper(
                subject_identifier=appt_id)

            if helper.hiv_status == POS:
                pos += 1

            elif helper.hiv_status == NEG:
                neg += 1

            elif helper.hiv_status == IND:
                ind += 1

        statistics.update(
            pos=pos,
            neg=neg,
            ind=ind
        )
        return statistics

    @property
    def enrollment_hiv_statistics(self):
        """Completed visit HIV statistics"""
        return self.get_hiv_statistics(appt_status=COMPLETE_APPT)

    @property
    def incomplete_enrol_hiv_statistics(self):
        """Inprogress visit HIV statistics"""
        return self.get_hiv_statistics(appt_status=IN_PROGRESS_APPT)
    
    @property
    def complete_appointment_count(self):
        facet_subject_identifiers = self.facet_consent_cls.objects.values_list(
            'subject_identifier', flat=True)
        
        appt_count =  self.facet_appointment_cls.objects.filter(
            appt_status = COMPLETE_APPT,
            subject_identifier__in = facet_subject_identifiers).count()
        
        return appt_count


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        facet_screenig = self.facet_subject_screening_cls.objects.all()
        facet_consent = self.facet_consent_cls.objects.all()
        focus_group = self.facet_focus_group_cls.objects.all()
        flourish_consents = self.flourish_consent_cls.objects.all()

        eligible_subjects = self.eligible_participants(
            flourish_consents).count()

        screened_subjects = facet_screenig.count()
        consented_subjects = facet_consent.count()
        facet_focus_groups = focus_group.count()

        context.update(
            consented_subjects=consented_subjects,
            screened_subjects=screened_subjects,
            facet_focus_groups=facet_focus_groups,
            complete_appointment_count=self.complete_appointment_count,
            eligible_subjects=eligible_subjects,
            consented_hiv_statistics=self.consented_hiv_statistics,
            screened_hiv_statistics=self.screened_hiv_statistics,
            appointment_statistics=self.appointment_statistics,
            enrollment_hiv_statistics=self.enrollment_hiv_statistics,
            incomplete_enrol_hiv_statistics=self.incomplete_enrol_hiv_statistics)

        return context
