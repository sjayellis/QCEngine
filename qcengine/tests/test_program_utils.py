"""
Tests the DQM compute dispatch module
"""

import pytest

import qcengine as qcng
from qcengine import testing


def test_list_programs():

    r = qcng.list_all_programs()
    assert r >= {"psi4", "rdkit", "molpro", "dftd3"}


@pytest.mark.parametrize("program", [
    pytest.param("psi4", marks=testing.using_psi4),
    pytest.param("torchani", marks=testing.using_torchani),
    pytest.param("rdkit", marks=testing.using_rdkit),
])
def test_check_program_avail(program):

    assert program in qcng.list_available_programs()


def test_program_avail_bounce():

    with pytest.raises(ValueError) as exc:
        qcng.compute({}, "bad_program", raise_error=True)

    assert "not registered" in str(exc.value)


def test_list_procedures():

    r = qcng.list_all_procedures()
    assert r >= {"geometric"}


@pytest.mark.parametrize("procedure", [
    pytest.param("geometric", marks=testing.using_geometric),
])
def test_check_procedure_avail(procedure):

    assert procedure in qcng.list_available_procedures()


def test_procedure_avail_bounce():

    with pytest.raises(ValueError) as exc:
        qcng.compute_procedure({}, "bad_program", raise_error=True)

    assert "not registered" in str(exc.value)