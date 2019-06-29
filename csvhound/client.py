#!/usr/bin/env python
"""
Start of csvhound full screen CLI powered by python-prompt-toolkit.
"""
import csvhound.core
from csvhound.cli import cli

hound_cli = cli.HoundCli()
hound_cli.create_application()
hound_cli.run_application()
