# Copyright 2012-2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import operator

import odoo.orm.domains as orm_domains
from odoo import api, fields, models


class FetchmailServer(models.Model):
    """Incoming POP/IMAP mail server account"""

    _name = "fetchmail.server"
    _inherit = ["fetchmail.server", "server.env.mixin"]

    @property
    def _server_env_fields(self):
        base_fields = super()._server_env_fields
        mail_fields = {
            "server": {},
            "port": {},
            "server_type": {},
            "user": {},
            "password": {},
            "is_ssl": {},
            "attach": {},
            "original": {},
        }
        mail_fields.update(base_fields)
        return mail_fields

    is_ssl = fields.Boolean(search="_search_is_ssl")
    server_type = fields.Selection(search="_search_server_type")

    @api.model
    def _server_env_global_section_name(self):
        """Name of the global section in the configuration files

        Can be customized in your model
        """
        return "incoming_mail"

    @api.model
    def _search_is_ssl(self, oper, value):
        """Keep the is_ssl field searchable to allow domain in search view."""
        if not isinstance(value, bool):
            return orm_domains._FALSE_LEAF
        operators = {
            "=": operator.eq,
            "!=": operator.ne,
        }
        if oper not in operators:
            return orm_domains._FALSE_LEAF
        servers = self.search([]).filtered(lambda s: operators[oper](value, s.is_ssl))  # pylint: disable=W8163
        return [("id", "in", servers.ids)]

    @api.model
    def _search_server_type(self, oper, value):
        operators = {
            "=": operator.eq,
            "!=": operator.ne,
            "in": operator.contains,
            "not in": lambda a, b: not operator.contains(a, b),
        }
        if oper not in operators:
            return [("id", "in", [])]
        servers = self.search([]).filtered(  # pylint: disable=W8163
            lambda s: operators[oper](value, s.server_type)
        )
        return [("id", "in", servers.ids)]
