import pytest

from test_fixtures import model, empty_model
from frewpy import FrewModel
from frewpy.models.exceptions import FrewError


def test_first_material(model):
    assert model.soil.get_materials()[0] == "Made Ground"


def test_fifth_material(model):
    assert model.soil.get_materials()[4] == "LC A - drained"


def test_no_materials(empty_model):
    with pytest.raises(FrewError):
        empty_model.soil.get_materials()


def test_get_material_properties_not_string(model):
    with pytest.raises(FrewError):
        model.soil.get_material_properties(3)


def test_get_material_properties_no_materials(empty_model):
    with pytest.raises(FrewError):
        empty_model.soil.get_material_properties("Dirt")


def test_get_material_properties_missing_material(model):
    with pytest.raises(FrewError):
        model.soil.get_material_properties("Dirt")


def test_get_material_properties(model):
    properties = model.soil.get_material_properties("Made Ground")
    assert properties["Colour"] == "NO_RGB"
    assert properties["UnitWeight"] == 20000.0
    assert properties["Phi"] == 30.0
    assert properties["Wallsoilfric_ratio"] == 0.6700000166893005
    assert properties["Phimax"] == 35.0
