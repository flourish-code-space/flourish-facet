from django.db import models
from edc_base.sites import SiteModelMixin
from edc_base.model_mixins import BaseUuidModel
from ...choices import TRANSCRIPTION_HOURS, FACET_STAFF
from edc_base.model_validators import date_not_future
from edc_protocol.validators import date_not_before_study_start
from edc_base.utils import get_utcnow
from edc_base.model_validators import datetime_not_future
from edc_protocol.validators import datetime_not_before_study_start
from django.core.validators import FileExtensionValidator


class FocusGroupInterviewTranscriptionAndTranslation(SiteModelMixin, BaseUuidModel):

    report_datetime = models.DateTimeField(
        verbose_name="Report Date",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future],
        default=get_utcnow,
        help_text=('If reporting today, use today\'s date/time, otherwise use '
                   'the date/time this information was reported.'))
    group_identifier = models.CharField(
        verbose_name='Group identifier',
        max_length=50,)

    transcription_date = models.DateField(
        verbose_name='Date transcription completed',
        validators=[date_not_before_study_start, date_not_future],
    )

    facet_member_transcription = models.CharField(
        verbose_name='Which FACET staff member completed the transcription and translation?',
        choices=FACET_STAFF,
        max_length=10,
    )
    transcription_duration = models.CharField(
        verbose_name=(
            'Approximately how long did it take to complete the transcription and translation?'),
        choices=TRANSCRIPTION_HOURS,
        max_length=10,
    )

    class Meta:
        app_label = 'flourish_facet'
        verbose_name = 'Focus Group Interview Transcription And Translation'
        verbose_name_plural = 'Focus Group Interview Transcription And Translation'
