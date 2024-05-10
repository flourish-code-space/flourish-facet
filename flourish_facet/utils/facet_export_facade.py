from django.http.request import HttpRequest
from flourish_export.views.export_methods_view_mixin import ExportMethodsViewMixin
from flourish_export.admin_export_helper import AdminExportHelper
from flourish_export.identifiers import ExportIdentifier


class FacetExportFacade(ExportMethodsViewMixin):

    def __init__(self, request: HttpRequest):
        self.app_label = 'flourish_facet'
        self.emails = []
        self.admin_helper_cls = AdminExportHelper
        self.export_identifier_cls = ExportIdentifier
        self.request = request

    def add_email(self, email):
        self.emails.append(email)

    def generate_export(self):
        super().generate_export(self.app_label, self.emails)
