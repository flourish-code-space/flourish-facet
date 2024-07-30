from django.db import models
from ...choices import WEIGHT_RECORDED
from ..model_mixins import CrfModelMixin
from edc_constants.choices import YES_NO
from django.core.validators import MinValueValidator, MaxValueValidator


class ChildAnthropometry(CrfModelMixin):

    has_oedema = models.CharField(
        verbose_name='Does the child have oedema of both feet?',
        choices=YES_NO,
        max_length=5
    )

    weight_1 = models.DecimalField(
        verbose_name='Child’s weight',
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(2.0), MaxValueValidator(13.0)],
        help_text="Measured in Kilograms (kg)"
    )

    weight_recorded = models.CharField(
        verbose_name='How was weight recorded?',
        choices=WEIGHT_RECORDED,
        max_length=50
    )

    length_1 = models.DecimalField(
        verbose_name='Child’s length',
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(40), MaxValueValidator(125)],
        help_text="Measured in Centimeters (cm)"
    )

    class Meta:
        app_label = 'flourish_facet'
        verbose_name = 'Child Anthropomentry'
        verbose_name_plural = 'Child Anthropomentry'
