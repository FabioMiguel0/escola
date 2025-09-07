# Pacote services - reexporta funções úteis do módulo db
from .db import get_conn, get_connection, create_tables_and_seed

__all__ = ["get_conn", "get_connection", "create_tables_and_seed"]

# Please note that script execution policies may vary based on system settings.
# If you encounter an error regarding script execution being disabled,
# you may need to adjust your system's execution policy to allow the script to run.
# This can typically be done by running PowerShell as an administrator and executing the command:
# Set-ExecutionPolicy RemoteSigned
# However, exercise caution and ensure you understand the implications of changing the execution policy.