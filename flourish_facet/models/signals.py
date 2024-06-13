from dateutil.relativedelta import relativedelta
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db import transaction
from django.apps import apps as django_apps
from edc_visit_schedule import site_visit_schedules
from edc_constants.constants import POS
from flourish_child.helper_classes.utils import stamp_image
from .clinicial_notes import ClinicianNotesImage
from .mother import FacetConsent
from .child import MotherChildConsent
from .child import ChildHivTesting
from ..models import FacetChildOffSchedule, FacetMotherOffSchedule

from ..action_items import FacetChildOffStudyAction

from ..utils import trigger_action_item
from ..action_items import (
    FACET_MOTHER_OFFSTUDY_ACTION, FACET_CHILD_OFFSTUDY_ACTION)
from ..utils import get_facet_child_schedule, get_facet_mother_schedule
from edc_data_manager.models import DataActionItem


@receiver(post_save, weak=False, sender=FacetConsent,
          dispatch_uid='facet_consent_on_post_save')
def facet_consent_on_post_save(sender, instance, raw, created, **kwargs):
    """
    - Put mother on schedule
    """

    with transaction.atomic():
        _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
            onschedule_model='flourish_facet.onschedulefacetmother',
            name='mother_facet_schedule'
        )

        schedule.put_on_schedule(
            subject_identifier=instance.subject_identifier,
            schedule_name='mother_facet_schedule'
        )

        for child_consent in instance.motherchildconsent_set.all():

            participant_note_cls = django_apps.get_model(
                'flourish_calendar.participantnote')

            if child_consent.child_dob:

                schedule_date = child_consent.child_dob + \
                    relativedelta(months=6)

                subject_identifier = instance.subject_identifier

                try:
                    participant_note_cls.objects.get(
                        subject_identifier=subject_identifier,
                        date=schedule_date
                    )

                except participant_note_cls.DoesNotExist:

                    participant_note_cls.objects.create(
                        subject_identifier=subject_identifier,
                        date=schedule_date,
                        title=f'FACET 6 Months follow up',
                        description=f'{child_consent.subject_identifier} turned 6 months',
                        color=None
                    )


@receiver(post_save, weak=False, sender=MotherChildConsent,
          dispatch_uid='facet_consent_on_post_save')
def facet_child_consent_on_post_save(sender, instance, raw, created, **kwargs):
    """
    - Put child on schedule
    """
    with transaction.atomic():

        _, child_schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
            onschedule_model='flourish_facet.onschedulefacetchild',
            name='child_facet_schedule'
        )

        child_schedule.put_on_schedule(
            subject_identifier=instance.subject_identifier,
            schedule_name='child_facet_schedule'
        )

        DataActionItem.objects.update_or_create(
            subject='Complete CREDI FORM on REDCAP',
            subject_identifier=instance.subject_identifier,
            assigned='clinic',
            comment='''\
                    Flourish Facet has CREDI form ,please complete CREDI form on REDCAP
                    '''
        )


@receiver(post_save, weak=False, sender=ChildHivTesting,
          dispatch_uid='child_hiv_testing_on_post_save')
def facet_child_hiv_testing_on_post_save(sender, instance, raw, created, **kwargs):

    if instance.hiv_result_6_weeks == POS:
        child_subject_identifier = instance.facet_visit.subject_identifier

        trigger_action_item(
            model_cls=FacetChildOffSchedule,
            action_name=FACET_CHILD_OFFSTUDY_ACTION,
            subject_identifier=child_subject_identifier,
            repeat=False,
        )


@receiver(post_save, weak=False, sender=FacetChildOffSchedule,
          dispatch_uid='facet_child_off_schedule_on_post_save')
def facet_child_off_schedule_on_post_save(sender, instance, raw, created, **kwargs):
    """
    - Put child off-schedule
    """
    with transaction.atomic():

        subject_identifier = instance.subject_identifier

        child_schedule = get_facet_child_schedule()

        if child_schedule.is_onschedule(subject_identifier=subject_identifier,
                                        report_datetime=instance.report_datetime):

            child_schedule.take_off_schedule(
                subject_identifier=subject_identifier,
                offschedule_datetime=instance.report_datetime)


@receiver(post_save, weak=False, sender=FacetMotherOffSchedule,
          dispatch_uid='facet_mother_off_schedule_on_post_save')
def facet_mother_off_schedule_on_post_save(sender, instance, raw, created, **kwargs):
    """
    - Put mother off-schedule
    """
    with transaction.atomic():

        subject_identifier = instance.subject_identifier

        schedule = get_facet_mother_schedule()

        if schedule.is_onschedule(subject_identifier=subject_identifier,
                                  report_datetime=instance.report_datetime):

            schedule.take_off_schedule(
                subject_identifier=subject_identifier,
                offschedule_datetime=instance.report_datetime)


@receiver(post_save, weak=False, sender=ClinicianNotesImage,
          dispatch_uid='facet_clinician_notes_image_on_post_save')
def facet_clinician_notes_image_on_post_save(sender, instance, raw, created, **kwargs):
    if not raw and created:
        stamp_image(instance)
