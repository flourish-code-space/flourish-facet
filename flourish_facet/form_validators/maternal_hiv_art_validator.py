from edc_form_validators import FormValidator
from edc_constants.constants import NO, YES, POS
from django.core.exceptions import ValidationError
from flourish_caregiver.helper_classes import MaternalStatusHelper


class MaternalHivArtFormValidator(FormValidator):
    def clean(self):
        super().clean()

        subject_identifier = self.cleaned_data.get(
            'facet_visit').subject_identifier

        status = MaternalStatusHelper(subject_identifier=subject_identifier)

        if status.hiv_status == POS:
            self.hiv_positive_validations()
        else:
            self.hiv_negative_validations()
        self.validate_against_hiv_test_date()

    def hiv_positive_validations(self):
    


        self.required_if(
            YES,
            field='art_received',
            field_required='drug_combination_before')

        self.validate_other_specify(field='drug_combination_before',
                                    other_specify_field='drug_combination_before_other')

        art_received_preg_fields = ('drug_combination_during',
                                    'art_switch')

        for field in art_received_preg_fields:

            self.required_if(
                YES,
                field='art_received_preg',
                field_required=field
            )
        art_regimen_switch = ('art_regimen',
                              'art_regimen_start',
                              'reason_regimen_change',)

        for art_field in art_regimen_switch:
            self.required_if(
                YES,
                field='art_switch', field_required=art_field
            )

        self.validate_other_specify(field='drug_combination_during',
                                    other_specify_field='drug_combination_during_other')

        self.validate_other_specify(field='art_regimen',
                                    other_specify_field='art_regimen_other')

        self.validate_other_specify(field='reason_regimen_change',
                                    other_specify_field='reason_regimen_change_other')

        self.m2m_other_specify(m2m_field='art_challenges',
                               field_other='art_challenges_other')

    def hiv_negative_validations(self):

        self.required_if(NO, field='father_hiv',
                         field_required='father_hiv_no')

        self.required_if('dont_know', field='father_hiv_no',
                         field_required='father_hiv_dont', inverse=True)

        status_required_fields = [
            'hiv_test_date_father', 'father_art', 'hiv_status_disclosure']

        hiv_result_father = self.cleaned_data.get('hiv_result_father', None)

        for field in status_required_fields:
            self.required_if_true(hiv_result_father, field_required=field)

        self.required_if(YES,
                         field='father_art',
                         field_required='father_art_start')

        self.m2m_required_if(YES, field='hiv_status_disclosure',
                             m2m_field='hiv_status_disclosure_reaction')

        self.required_if(NO, field='hiv_status_disclosure',
                         field_required='comment_end')
        
    def validate_against_hiv_test_date(self):
        cleaned_data = self.cleaned_data
        hiv_test_date = cleaned_data.get('hiv_test_date')
        art_start_date = cleaned_data.get('art_start_date')
        if (art_start_date and art_start_date < hiv_test_date):
            msg ={'art_start_date':
                       'Date cannot be before date tested positive '
                       f' {hiv_test_date}'}
            raise ValidationError(msg)
