# Copyright Contributors to the Packit project.
# SPDX-License-Identifier: MIT

"""
Validate PackageConfig
"""

import logging
import os
from typing import Optional

import click

from packit.api import PackitAPI
from packit.cli.types import LocalProjectParameter
from packit.cli.utils import cover_packit_exception
from packit.config import get_context_settings
from packit.local_project import LocalProject

logger = logging.getLogger(__name__)


@click.command("validate", context_settings=get_context_settings())
@click.argument("path_or_url", type=LocalProjectParameter(), default=os.path.curdir)
@click.option(
    "--offline",
    default=False,
    is_flag=True,
    help="Do not make remote API calls requiring network access.",
)
@click.option(
    "-c",
    "--config-path",
    type=click.Path(exists=True),
    help="Path to a specific Packit configuration file.",
)
@cover_packit_exception
def validate_config(
    path_or_url: LocalProject,
    offline: bool,
    config_path: Optional[str] = None,
):
    """
    Validate PackageConfig.

    \b
    - checks missing values
    - checks incorrect types
    - checks whether monitoring is enabled if 'pull_from_upstream` is used

    PATH_OR_URL argument is a local path or a URL to a git repository with packit configuration file
    config: Optional path to a specific Packit configuration file.
    """

    output = PackitAPI.validate_package_config(
        path_or_url.working_dir,
        offline,
        config_path,
    )
    logger.info(output)
    # TODO: print more if config.debug
