"""
Tests the DQM compute dispatch module
"""

import copy

import numpy as np
import pytest
from qcelemental.models import OptimizationInput

import qcengine as qcng
from qcengine import testing

_base_json = {
    "schema_name": "qcschema_optimization_input",
    "schema_version": 1,
    "keywords": {
        "coordsys": "tric",
        "maxiter": 100,
        "program": None
    },
    "input_specification": {
        "schema_name": "qcschema_input",
        "schema_version": 1,
        "driver": "gradient",
        "model": None,
        "keywords": {},
    },
    "initial_molecule": None
}


def _bond_dist(geom, a1, a2):
    """
    Computes a simple bond distance between two rows in a flat (n, 3) list of coordinates
    """
    if isinstance(geom, np.ndarray):
        geom = geom.flatten().tolist()
    a13 = a1 * 3
    a23 = a2 * 3

    xd = (geom[a13] - geom[a23])**2
    yd = (geom[a13 + 1] - geom[a23 + 1])**2
    zd = (geom[a13 + 2] - geom[a23 + 2])**2

    return (xd + yd + zd)**0.5


@testing.using_psi4
@testing.using_geometric
def test_geometric_psi4():
    inp = copy.deepcopy(_base_json)

    inp["initial_molecule"] = qcng.get_molecule("hydrogen")
    inp["input_specification"]["model"] = {"method": "HF", "basis": "sto-3g"}
    inp["keywords"]["program"] = "psi4"

    inp = OptimizationInput(**inp)

    ret = qcng.compute_procedure(inp, "geometric", raise_error=True)
    assert 10 > len(ret.trajectory) > 1

    assert pytest.approx(ret.final_molecule.measure([0, 1]), 1.e-4) == 1.3459150737
    assert ret.provenance.creator.lower() == "geometric"
    assert ret.trajectory[0].provenance.creator.lower() == "psi4"


@testing.using_psi4
@testing.using_geometric
def test_geometric_local_options():
    inp = copy.deepcopy(_base_json)

    inp["initial_molecule"] = qcng.get_molecule("hydrogen")
    inp["input_specification"]["model"] = {"method": "HF", "basis": "sto-3g"}
    inp["keywords"]["program"] = "psi4"

    inp = OptimizationInput(**inp)

    # Set some extremely large number to test
    ret = qcng.compute_procedure(inp, "geometric", raise_error=True, local_options={"memory": "5000"})
    assert pytest.approx(ret.trajectory[0].provenance.memory, 1) == 4900

    # Make sure we cleaned up
    assert "_qcengine_local_config" not in ret.input_specification
    assert "_qcengine_local_config" not in ret.trajectory[0].extras


@testing.using_rdkit
@testing.using_geometric
def test_geometric_stdout():
    inp = copy.deepcopy(_base_json)

    inp["initial_molecule"] = qcng.get_molecule("water")
    inp["input_specification"]["model"] = {"method": "UFF", "basis": ""}
    inp["keywords"]["program"] = "rdkit"

    inp = OptimizationInput(**inp)

    ret = qcng.compute_procedure(inp, "geometric", raise_error=True)
    assert ret.success is True
    assert "Converged!" in ret.stdout


@testing.using_rdkit
@testing.using_geometric
def test_geometric_rdkit_error():
    inp = copy.deepcopy(_base_json)

    inp["initial_molecule"] = qcng.get_molecule("water").copy(exclude={"connectivity"})
    inp["input_specification"]["model"] = {"method": "UFF", "basis": ""}
    inp["keywords"]["program"] = "rdkit"

    inp = OptimizationInput(**inp)

    ret = qcng.compute_procedure(inp, "geometric")
    assert ret.success is False
    assert isinstance(ret.error.error_message, str)


@testing.using_torchani
@testing.using_geometric
def test_geometric_torchani():
    inp = copy.deepcopy(_base_json)

    inp["initial_molecule"] = qcng.get_molecule("water")
    inp["input_specification"]["model"] = {"method": "ANI1", "basis": None}
    inp["keywords"]["program"] = "torchani"

    ret = qcng.compute_procedure(inp, "geometric", raise_error=True)
    assert ret.success is True
    assert "Converged!" in ret.stdout
