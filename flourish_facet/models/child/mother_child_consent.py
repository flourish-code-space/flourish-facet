from django.db import models
from edc_base.utils import age, get_utcnow
from ..mother import FacetConsent
from django_crypto_fields.fields import FirstnameField, LastnameField
from django_crypto_fields.fields import IdentityField
from edc_constants.choices import GENDER, YES_NO
from ...choices import CHILD_IDENTITY_TYPE, CHILD_CONSENT_VERSION
from edc_base.model_validators import datetime_not_future, date_not_future
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierFieldMixin
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_consent.field_mixins import IdentityFieldsMixin
from edc_consent.field_mixins import PersonalFieldsMixin
from edc_protocol.validators import datetime_not_before_study_start
from django.core.validators import MaxValueValidator, MinValueValidator
from edc_consent.field_mixins import VerificationFieldsMixin
from edc_base.model_mixins import BaseUuidModel
from .child_consent_eligibility import ChildConsentEligibility
from edc_search.model_mixins import SearchSlugModelMixin


class MotherChildConsent(SiteModelMixin, NonUniqueSubjectIdentifierFieldMixin, SearchSlugModelMixin,
                         IdentityFieldsMixin, PersonalFieldsMixin, BaseUuidModel):
    facet_consent = models.ForeignKey(
        FacetConsent,
        on_delete=models.PROTECT
    )

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=50)

    first_name = FirstnameField(
        verbose_name="First name",
        blank=True,
        null=True
    )

    last_name = LastnameField(
        verbose_name="Last name",
        blank=True,
        null=True
    )

    gender = models.CharField(
        verbose_name="Gender",
        choices=GENDER,
        max_length=1, )

    identity = IdentityField(
        verbose_name='Identity number',
        null=True,
        blank=True)

    identity_type = models.CharField(
        verbose_name='What type of identity number is this?',
        max_length=25,
        choices=CHILD_IDENTITY_TYPE,
        null=True,
        blank=True)

    confirm_identity = IdentityField(
        help_text='Retype the identity number',
        null=True,
        blank=True)

    child_dob = models.DateField(
        verbose_name="Date of birth",
        validators=[date_not_future, ],
        null=True,
        blank=True)

    child_test = models.CharField(
        verbose_name='Will you allow for HIV testing and counselling of '
                     'your Child',
        max_length=5,
        choices=YES_NO,
        help_text='If no, participant is not eligible.')

    consent_datetime = models.DateTimeField(
        verbose_name='Consent date and time',
        validators=[
            datetime_not_before_study_start,
            datetime_not_future])

    is_eligible = models.BooleanField(
        default=False,
        editable=False)

    version = models.CharField(default='1', max_length=3)

    @property
    def consent_version(self):
        return self.version

    def get_search_slug_fields(self):
        fields = super().get_search_slug_fields()
        fields.append('subject_identifier')
        return fields

    def save(self, *args, **kwargs):
        eligibile = ChildConsentEligibility(
            child_dob=self.consent_datetime.date(),
            child_test=self.child_test,
            consent_date=self.consent_datetime.date()
        )

        self.is_eligible = eligibile.is_eligible

        return super().save(*args, **kwargs)

    class Meta:
        app_label = 'flourish_facet'
        verbose_name = 'Mother Consent On Behalf Of Child'
        verbose_name_plural = 'Mother Consent On Behalf Of Child'
