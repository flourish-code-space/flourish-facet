from django.apps import apps as django_apps
from django.db.models import Q
from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import SearchFormViewMixin
from edc_dashboard.views import ListboardView
from edc_navbar import NavbarViewMixin
from flourish_facet.views.eligible_facet_participants_mixin import EligibleFacetParticipantsMixin
from ...model_wrappers import FlourishConsentModelWrapper


class FlourishConsentListboardView(EdcBaseViewMixin,
                                   NavbarViewMixin,
                                   SearchFormViewMixin,
                                   ListboardView,
                                   EligibleFacetParticipantsMixin):

    listboard_template = 'facet_flourish_consent_template'
    listboard_url = 'facet_flourish_consent_listboard_url'
    listboard_panel_style = 'success'
    listboard_fa_icon = "far fa-user-circle"
    search_form_url = 'facet_flourish_consent_listboard_url'

    model = 'flourish_caregiver.subjectconsent'
    model_wrapper_cls = FlourishConsentModelWrapper
    navbar_name = 'flourish_facet'
    navbar_selected_item = 'facet_flourish_consent_listboard_url'

    flourish_child_consent_model = 'flourish_caregiver.caregiverchildconsent'

    def get_queryset_filter_options(self, request, *args, **kwargs):
        options = super().get_queryset_filter_options(request, *args, **kwargs)
        if kwargs.get('subject_identifier'):
            options.update(
                {'subject_identifier': kwargs.get('subject_identifier')})
        return options

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        facet_screening_add_url = ('/admin/flourish_facet/facetsubjectscreening/add/?'
                                   'next=flourish_facet:facet_flourish_consent_listboard_url')

        context.update(
            facet_screening_add_url=facet_screening_add_url)

        return context

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        return self.eligible_participants(queryset)
