"""Code for converting notebooks to and from v5."""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

import json
import re

from .nbbase import (
    nbformat, nbformat_minor,
    NotebookNode,
)

from nbformat import v4
from traitlets.log import get_logger

def _warn_if_invalid(nb, version):
    """Log validation errors, if there are any."""
    from nbformat import validate, ValidationError
    try:
        validate(nb, version=version)
    except ValidationError as e:
        get_logger().error("Notebook JSON is not valid v%i: %s", version, e)

def upgrade(nb, from_version=4, from_minor=0):
    """Convert a notebook to v5.

    Parameters
    ----------
    nb : NotebookNode
        The Python representation of the notebook to convert.
    from_version : int
        The original version of the notebook to convert.
    from_minor : int
        The original minor version of the notebook to convert (only relevant for v >= 3).
    """
    print('Entering convert.py upgrade()')
    if from_version == 4:
        # Validate the notebook before conversion
        _warn_if_invalid(nb, from_version)

        # Mark the original nbformat so consumers know it has been converted
        orig_nbformat = nb.pop('orig_nbformat', None)
        orig_nbformat_minor = nb.pop('orig_nbformat_minor', None)
        nb.metadata.orig_nbformat = orig_nbformat or 4
        nb.metadata.orig_nbformat_minor = orig_nbformat_minor or 0

        # Mark the new format
        nb.nbformat = nbformat
        nb.nbformat_minor = nbformat_minor

        # No changes necessary to cells from v4
        cells=nb['cells'] #probably do not need
        # Validate the converted notebook before returning it
        _warn_if_invalid(nb, nbformat)
        return nb
    elif from_version == 5:
        # nothing to do
        if from_minor != nbformat_minor:
            nb.metadata.orig_nbformat_minor = from_minor
        nb.nbformat_minor = nbformat_minor

        return nb
    else:
        raise ValueError('Cannot convert a notebook directly from v%s to v5.  ' \
                'Try using the nbformat.convert module.' % from_version)

def upgrade_cell(cell):
    """upgrade a cell from v4 to v5

    nothing to do
    """
    print('entering convert.py upgrade_cell()')
    return cell

def downgrade_cell(cell):
    """downgrade a cell from v5 to v4

    WYSIWYG -> markdown, since markdown also handles html.
    """
    print('entering convert.py downgrade_cell()')
    if cell.cell_type == 'WYSIWYG':
        cell.cell_type = 'markdown'
        cell.source = text
    return cell

_mime_map = {
    "text" : "text/plain",
    "html" : "text/html",
    "svg" : "image/svg+xml",
    "png" : "image/png",
    "jpeg" : "image/jpeg",
    "latex" : "text/latex",
    "json" : "application/json",
    "javascript" : "application/javascript",
};

def to_mime_key(d):
    """nothing to do"""
    print('entering convert.py to_mime_key()')
    return d

def from_mime_key(d):
    """nothing to do"""
    return d

def upgrade_output(output):
    """upgrade a single code cell output from v4 to v5

    nothing to do
    """
    print('entering convert.py upgrade_output()')
    return output

def downgrade_output(output):
    """downgrade a single code cell output to v4 from v5

    -Will need to keep the html version of the WYSIWYG
    """
    return output

def upgrade_outputs(outputs):
    """upgrade outputs of a code cell from v4 to v5"""
    print('entering convert.py upgrade_outputs()')
    return [upgrade_output(op) for op in outputs]

def downgrade_outputs(outputs):
    """downgrade outputs of a code cell to v4 from v5"""
    return [downgrade_output(op) for op in outputs]

def downgrade(nb):
    """Convert a v5 notebook to v4.

    Parameters
    ----------
    nb : NotebookNode
        The Python representation of the notebook to convert.
    """
    print('entering convert.py downgrade()')
    if nb.nbformat != nbformat:
        return nb

    # Validate the notebook before conversion
    _warn_if_invalid(nb, nbformat)

    nb.nbformat = v4.nbformat
    nb.nbformat_minor = v4.nbformat_minor
    cells = [ downgrade_cell(cell) for cell in nb.pop('cells') ]
    nb['cells']=cells
    nb.metadata.setdefault('name', '')

    # Validate the converted notebook before returning it
    _warn_if_invalid(nb, v4.nbformat)

    nb.orig_nbformat = nb.metadata.pop('orig_nbformat', nbformat)
    nb.orig_nbformat_minor = nb.metadata.pop('orig_nbformat_minor', nbformat_minor)

    return nb
