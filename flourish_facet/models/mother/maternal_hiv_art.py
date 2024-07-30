from django.db import models
from ..model_mixins import CrfModelMixin
from edc_constants.choices import YES_NO, YES_NO_DONT_KNOW
from ...choices import DRUG_COMBINATION, POS_NEG_IND, REASONS_REGIMEN_CHANGE
from edc_base.model_fields import OtherCharField
from ..list_models import ArtChallenges, PartnerReaction
from edc_base.model_validators.date import date_not_future


class MaternalHivArt(CrfModelMixin):

    hiv_test_date = models.DateField(
        verbose_name='When did you first test positive for HIV?',
        null=True,
        blank=False,
        validators=[date_not_future]
    )
    art_received = models.CharField(
        verbose_name=(
            'Did you receive antiretroviral therapy (ART)'' before you became pregnant with this child?'),
        choices=YES_NO,
        blank=True,
        null=True,
        max_length=5,
    )

    drug_combination_before = models.CharField(
        verbose_name=(
            'If yes, specify the last (most recent) drug''/combination of drugs received before this pregnancy?'),
        choices=DRUG_COMBINATION,
        max_length=50,
        blank=True,
        null=True,
    )
    drug_combination_before_other = OtherCharField()

    art_start_date = models.DateField(
        verbose_name='When did you start taking antiretroviral drugs?',
        null=True,
        blank=True,
        validators=[date_not_future,]
    )

    art_received_preg = models.CharField(
        verbose_name=(
            'Did you receive antiretroviral drugs'' during pregnancy with this child?'),
        choices=YES_NO,
        blank=True,
        max_length=5,
        null=True,
    )
    drug_combination_during = models.CharField(
        verbose_name=(
            'If yes, specify the last drug''/combination of drugs received during this pregnancy?'),
        choices=DRUG_COMBINATION,
        max_length=50,
        blank=True,
        null=True,
    )
    drug_combination_during_other = OtherCharField()

    art_switch = models.CharField(
        verbose_name='Did you switch ART regimen in the past year (including during pregnancy)',
        choices=YES_NO,
        max_length=5,
        blank=True,
        null=True,
    )

    art_regimen = models.CharField(
        verbose_name='If yes, what was the previous ART regimen',
        choices=DRUG_COMBINATION,
        max_length=50,
        blank=True,
        null=True,
    )
    art_regimen_other = OtherCharField()

    art_regimen_start = models.DateField(
        verbose_name='When did you start the previous ART regimen?',
        null=True,
        blank=True,
        validators=[date_not_future]
    )

    reason_regimen_change = models.CharField(
        verbose_name='Indicate reason for regimen change',
        choices=REASONS_REGIMEN_CHANGE,
        max_length=30,
        blank=True,
        null=True,
    )
    reason_regimen_change_other = OtherCharField()

    art_challenges = models.ManyToManyField(
        ArtChallenges,
        related_name='art_challenges',
        verbose_name="Challenges you have when taking all of the doses of ARVs",
        blank=True

    )
    art_challenges_other = OtherCharField()

    father_hiv = models.CharField(
        verbose_name='Has the father of the child ever been tested for HIV infection?',
        choices=YES_NO_DONT_KNOW,
        max_length=20,
        null=True,
        blank=True,
    )
    father_hiv_no = models.CharField(
        verbose_name='If no,Would the father be willing to be HIV tested?',
        choices=YES_NO_DONT_KNOW,
        max_length=20,
        null=True,
        blank=True,
    )
    father_hiv_dont = models.CharField(
        verbose_name='If unsure ,Would the father be willing to be HIV tested?',
        choices=YES_NO_DONT_KNOW,
        max_length=20,
        null=True,
        blank=True,
    )

    comment = models.TextField(
        verbose_name='Comment',
        max_length=250,
        blank=True,
        null=True)

    hiv_result_father = models.CharField(
        verbose_name="What was the result of the last HIV test?",
        choices=POS_NEG_IND,
        max_length=15,
        null=True,
        blank=True,)

    hiv_test_date_father = models.DateField(
        verbose_name='When did the father last test for HIV?',
        null=True,
        blank=True,
        validators=[date_not_future]
    )

    father_art = models.CharField(
        verbose_name='Is the father receiving ART?',
        choices=YES_NO_DONT_KNOW,
        max_length=20,
        null=True,
        blank=True,
    )

    father_art_start = models.DateField(
        verbose_name='When did he start ART',
        null=True,
        blank=True,
        validators=[date_not_future]
    )

    hiv_status_disclosure = models.CharField(
        verbose_name='Since the last visit with flourish study ,have disclosed you HIV status to the father of your child ?',
        choices=YES_NO,
        max_length=5,
        blank=True,
        null=True,
    )

    hiv_status_disclosure_reaction = models.ManyToManyField(
        PartnerReaction,
        related_name='hiv_status_disclosure_reaction',
        verbose_name='When you disclosed you HIV status to the partner,what was his reaction',
        blank=True
    )

    comment_end = models.TextField(
        verbose_name=(
            'If you have not yet disclosed you HIV status to the father ,whats your reason'),
        blank=True,
        max_length=250,
        null=True)

    class Meta:
        app_label = 'flourish_facet'
        verbose_name = 'Maternal HIV ART'
        verbose_name_plural = 'Maternal HIV ART'
