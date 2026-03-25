def uninstall_hook(env):
    """Restore database columns that server.env.mixin dropped for mail models.

    When mail_environment is uninstalled, ``ir.mail_server`` and
    ``fetchmail.server`` would be left without the columns that the ORM
    dropped when this addon was first installed. This hook recreates those
    columns and repopulates them with the current effective values so the
    database remains usable after removal.
    """
    mixin = env["server.env.mixin"]
    mixin.restore_env_managed_columns(
        "ir.mail_server",
        [
            "smtp_host",
            "smtp_port",
            "smtp_user",
            "smtp_pass",
            "smtp_encryption",
            "smtp_authentication",
        ],
    )
    mixin.restore_env_managed_columns(
        "fetchmail.server",
        [
            "server",
            "port",
            "server_type",
            "user",
            "password",
            "is_ssl",
            "attach",
            "original",
        ],
    )
