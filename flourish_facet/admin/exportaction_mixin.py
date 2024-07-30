import datetime
import uuid
from django.apps import apps as django_apps
from django.db.models import ManyToManyField, ForeignKey, OneToOneField, ManyToOneRel, FileField, ImageField
from django.db.models.fields.reverse_related import OneToOneRel
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from flourish_export.admin_export_helper import AdminExportHelper
import xlwt
from flourish_caregiver.helper_classes import MaternalStatusHelper


class ExportActionMixin(AdminExportHelper):

    def update_variables(self, data={}):
        """ Update study identifiers to desired variable name(s).
        """
        replace_idx = {}
        for old_idx, new_idx in replace_idx.items():
            try:
                data[new_idx] = data.pop(old_idx)
            except KeyError:
                continue
        return data

    def study_status(self, subject_identifier=None):
        if not subject_identifier:
            return ''
        caregiver_offstudy_cls = django_apps.get_model(
            'flourish_prn.caregiveroffstudy')
        is_offstudy = caregiver_offstudy_cls.objects.filter(
            subject_identifier=subject_identifier).exists()

        return 'off_study' if is_offstudy else 'on_study'

    def export_as_csv(self, request, queryset):
        records = []

        for obj in queryset:
            data = obj.__dict__.copy()

            subject_identifier = getattr(obj, 'subject_identifier', None)
            screening_identifier = self.screening_identifier(
                subject_identifier=subject_identifier)
            caregiver_hiv_status = self.caregiver_hiv_status(
                subject_identifier=subject_identifier)

            # Add subject identifier and visit code
            if getattr(obj, 'facet_visit', None):
                data.update(
                    subject_identifier=subject_identifier,
                    visit_code=obj.visit_code)

            # Update variable names for study identifiers
            data = self.update_variables(data)
            data.update(study_status=self.study_status(subject_identifier) or '')
            data.update(hiv_status=caregiver_hiv_status,)

            for field in self.get_model_fields:
                field_name = field.name
                if (field_name == 'consent_version') and self.is_visit(obj):
                    data.update({f'{field_name}': '1'})
                    continue
                if isinstance(field, (ForeignKey, OneToOneField, OneToOneRel,)):
                    continue
                if isinstance(field, (FileField, ImageField,)):
                    file_obj = getattr(obj, field_name, '')
                    data.update({f'{field_name}': getattr(file_obj, 'name', '')})
                    continue
                if isinstance(field, ManyToManyField):
                    data.update(self.m2m_data_dict(obj, field))
                    continue
                if not (self.is_consent(obj) or self.is_visit(obj)) and isinstance(field, ManyToOneRel):
                    data.update(self.inline_data_dict(obj, field))
                    continue

            # Exclude identifying values
            data = self.remove_exclude_fields(data)
            # Correct date formats
            data = self.fix_date_formats(data)
            records.append(data)
        response = self.write_to_csv(records)
        return response

    export_as_csv.short_description = _(
        'Export selected %(verbose_name_plural)s')

    actions = [export_as_csv]

    def write_rows(self, data=None, row_num=None, ws=None):

        for col_num in range(len(data)):
            if isinstance(data[col_num], uuid.UUID):
                ws.write(row_num, col_num, str(data[col_num]))
            elif isinstance(data[col_num], datetime.datetime):
                dt = data[col_num]
                if dt.tzinfo is not None and dt.tzinfo.utcoffset(dt) is not None:
                    dt = timezone.make_naive(dt)
                dt = dt.strftime('%Y/%m/%d')
                ws.write(row_num, col_num, dt, xlwt.easyxf(
                    num_format_str='YYYY/MM/DD'))
            elif isinstance(data[col_num], datetime.date):
                ws.write(row_num, col_num, data[col_num], xlwt.easyxf(
                    num_format_str='YYYY/MM/DD'))
            else:
                ws.write(row_num, col_num, data[col_num])

    def update_headers_inline(self, inline_fields=None, field_names=None,
                              ws=None, row_num=None, font_style=None):
        top_num = len(field_names)
        for col_num in range(len(inline_fields)):
            ws.write(row_num, top_num, inline_fields[col_num], font_style)
            top_num += 1
            self.inline_header = True

    def get_export_filename(self):
        date_str = datetime.datetime.now().strftime('%Y-%m-%d')
        filename = "%s-%s" % (self.model.__name__, date_str)
        return filename

    def screening_identifier(self, subject_identifier=None):
        """Returns a screening identifier.
        """
        consent = self.consent_obj(subject_identifier=subject_identifier)

        if consent:
            return getattr(consent, 'screening_identifier', None)
        return None

    def caregiver_hiv_status(self, subject_identifier=None):

        status_helper = MaternalStatusHelper(
            subject_identifier=subject_identifier)

        return status_helper.hiv_status

    def consent_obj(self, subject_identifier: str):
        consent_cls = django_apps.get_model('flourish_facet.facetconsent')
        consent = consent_cls.objects.filter(
            subject_identifier=subject_identifier)

        if consent.exists():
            return consent.last()
        return None

    def is_consent(self, obj):
        consent_cls = django_apps.get_model('flourish_facet.facetconsent')
        return isinstance(obj, consent_cls)

    def is_visit(self, obj):
        visit_cls = django_apps.get_model('flourish_facet.facetvisit')
        return isinstance(obj, visit_cls)

    @property
    def get_model_fields(self):
        return [field for field in self.model._meta.get_fields()
                if field.name not in self.exclude_fields and not isinstance(field,
                                                                            OneToOneRel)]

    def inline_exclude(self, field_names=[]):
        return [field_name for field_name in field_names
                if field_name not in self.exclude_fields]

    @property
    def exclude_fields(self):
        return ['_state', 'hostname_created', 'hostname_modified',
                'revision', 'device_created', 'device_modified', 'id', 'site_id',
                'modified_time', 'report_datetime_time', 'registration_datetime_time',
                'screening_datetime_time', 'modified', 'form_as_json', 'consent_model',
                'randomization_datetime', 'registration_datetime', 'is_verified_datetime',
                'first_name', 'last_name', 'initials', 'identity', 'facet_visit_id',
                'confirm_identity', 'motherchildconsent', ]
