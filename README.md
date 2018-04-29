Het doel is om automatisch de metaalunievoorwaarden achter een pdf factuur toe te voegen.
Daarna misschien automatisch het mailprogramma openen met de juiste titel en bijlage etc.

Uses the `watchdog` and `openpyxl` packages.

Both `mail_subject` and `mail_body` accept the `{num}` formatting argument. It will be replaced with the invoice number.