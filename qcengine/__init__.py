"""
Base file for the dqm_compute module.
"""

from . import config
# Handle versioneer
from ._version import get_versions
from .compute import compute, compute_procedure
from .config import get_config, load_options
from .stock_mols import get_molecule

versions = get_versions()
__version__ = versions['version']
__git_revision__ = versions['full-revisionid']
del get_versions, versions
