"""flourish_facet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from flourish_facet.views.interview_forms.listboard_view import GroupInterviewListBoardView
from .admin_site import flourish_facet_admin
from django.urls import path
from django.apps import apps as django_apps
from edc_dashboard import UrlConfig
from django.views.generic.base import RedirectView
from django.apps import apps as django_apps
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path
from django.views.generic.base import RedirectView
from edc_action_item.admin_site import edc_action_item_admin
from edc_appointment.admin_site import edc_appointment_admin
from edc_identifier.admin_site import edc_identifier_admin
from .views import FacetMotherConsentListboardView
from .views import FlourishConsentListboardView
from .views import FacetChildConsentListboardView
from .views import FacetExportListBoardView
from .views import FacetMotherDashboardView
from .views import FacetChildDashboardView
from .views import AdministrationView, HomeView, CallHistoryView
from .patterns import subject_identifier, group_identifier
from .admin_site import flourish_facet_admin


app_name = 'flourish_facet'

app_config = django_apps.get_app_config(app_name)


urlpatterns = [
    path('admin/', flourish_facet_admin.urls),
    path('accounts/', include('edc_base.auth.urls')),
    path('admin/', include('edc_base.auth.urls')),

    path('admin/', admin.site.urls),
    path('admin/', flourish_facet_admin.urls),

    path('admin/', edc_identifier_admin.urls),
    path('admin/', edc_appointment_admin.urls),
    path('admin/', edc_action_item_admin.urls),

    path('administration/', AdministrationView.as_view(),
         name='administration_url'),
    path('home/', HomeView.as_view(), name='home_url'),
    path('', RedirectView.as_view(url='admin/'), name='admin_url'),
    re_path(r'^events/'
            f'(?P<subject_identifier>{subject_identifier})/',
            CallHistoryView.as_view(),
            name='callevent')

]

facet_mother_listboard_url_config = UrlConfig(
    url_name='facet_mother_listboard_url',
    view_class=FacetMotherConsentListboardView,
    label='facet_mother_listboard',
    identifier_label='subject_identifier',
    identifier_pattern=subject_identifier)

group_interview_listboard_url_config = UrlConfig(
    url_name='group_interview_listboard_url',
    view_class=GroupInterviewListBoardView,
    label='group_interview_listboard',
    identifier_label='group_identifier',
    identifier_pattern=group_identifier)

flourish_consent_listboard_url_config = UrlConfig(
    url_name='facet_flourish_consent_listboard_url',
    view_class=FlourishConsentListboardView,
    label='flourish_consent_listboard',
    identifier_label='subject_identifier',
    identifier_pattern=subject_identifier)


facet_mother_dashboard_url_config = UrlConfig(
    url_name='facet_mother_dashboard_url',
    view_class=FacetMotherDashboardView,
    label='facet_mother_dashboard',
    identifier_label='subject_identifier',
    identifier_pattern=subject_identifier)


facet_child_listboard_url_config = UrlConfig(
    url_name='facet_child_listboard_url',
    view_class=FacetChildConsentListboardView,
    label='facet_child_listboard',)


facet_child_dashboard_url_config = UrlConfig(
    url_name='facet_child_dashboard_url',
    view_class=FacetChildDashboardView,
    label='facet_child_dashboard',
    identifier_label='subject_identifier',
    identifier_pattern=subject_identifier)


facet_export_listboard_url_config = UrlConfig(
    url_name='facet_export_listboard_url',
    view_class=FacetExportListBoardView,
    label='facet_export_listboard_url',)

urlpatterns += facet_mother_listboard_url_config.listboard_urls
urlpatterns += flourish_consent_listboard_url_config.listboard_urls
urlpatterns += facet_mother_dashboard_url_config.dashboard_urls
urlpatterns += facet_child_listboard_url_config.listboard_urls
urlpatterns += facet_child_dashboard_url_config.dashboard_urls
urlpatterns += group_interview_listboard_url_config.listboard_urls
urlpatterns += facet_export_listboard_url_config.listboard_urls
