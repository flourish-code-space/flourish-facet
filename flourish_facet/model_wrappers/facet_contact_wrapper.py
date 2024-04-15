from django.conf import settings
from edc_model_wrapper import ModelWrapper


class FacetContactModelWrapper(ModelWrapper):

    model = 'flourish_caregiver.caregivercontact'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'facet_mother_dashboard_url')
    next_url_attrs = ['subject_identifier']
    querystring_attrs = ['subject_identifier', 'study_name']
