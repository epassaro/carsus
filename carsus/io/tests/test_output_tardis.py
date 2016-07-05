import pytest
import os

from carsus.io.output.tardis_op import AtomData
from carsus.model import DataSource
from numpy.testing import assert_almost_equal
from astropy import units as u
from astropy.tests.helper import assert_quantity_allclose


with_test_db = pytest.mark.skipif(
    not pytest.config.getoption("--test-db"),
    reason="--testing database was not specified"
)


@pytest.fixture
def atom_data(test_session):
    atom_data = AtomData(test_session, chianti_species=["He 2", "N 6"])
    return atom_data


@pytest.fixture
def atom_masses(atom_data):
    return atom_data.atom_masses


@pytest.fixture
def ionization_energies(atom_data):
    return atom_data.ionization_energies


@pytest.fixture
def levels(atom_data):
    return atom_data.levels


@pytest.fixture
def lines(atom_data):
    return atom_data.lines


@pytest.fixture
def collisions(atom_data):
    return atom_data.collisions


@pytest.fixture
def macro_atom(atom_data):
    return atom_data.macro_atom


@pytest.fixture
def macro_atom_references(atom_data):
    return atom_data.macro_atom_references


@pytest.fixture
def hdf5_path(request, data_dir):
    hdf5_path = os.path.join(data_dir, "test_hdf.hdf5")

    def fin():
      os.remove(hdf5_path)
    request.addfinalizer(fin)

    return hdf5_path


@with_test_db
@pytest.mark.parametrize("atomic_number, exp_mass", [
    (2, 4.002602),
    (11, 22.98976928)
])
def test_create_atom_masses(atom_masses, atomic_number, exp_mass):
    atom_masses = atom_masses.set_index("atomic_number")
    assert_almost_equal(atom_masses.loc[atomic_number]["mass"], exp_mass)


@with_test_db
def test_create_atom_masses_max_atomic_number(test_session):
    atom_data = AtomData(test_session, atom_masses_max_atomic_number=15)
    atom_masses = atom_data.atom_masses
    assert atom_masses["atomic_number"].max() == 15


@with_test_db
@pytest.mark.parametrize("atomic_number, ion_number, exp_ioniz_energy", [
    (8, 5, 138.1189),
    (11, 0,  5.1390767)
])
def test_create_ionizatinon_energies(ionization_energies, atomic_number, ion_number, exp_ioniz_energy):
    ionization_energies = ionization_energies.set_index(["atomic_number", "ion_number"])
    assert_almost_equal(ionization_energies.loc[(atomic_number, ion_number)]["ionization_energy"],
                        exp_ioniz_energy)


@with_test_db
@pytest.mark.parametrize("atomic_number, ion_number, level_number, exp_energy",[
    (7, 5, 7, 3991860.0 * u.Unit("cm-1")),
    (4, 2, 2, 981177.5 * u.Unit("cm-1"))
])
def test_create_levels(levels, atomic_number, ion_number, level_number, exp_energy):
    levels = levels.set_index(["atomic_number", "ion_number", "level_number"])
    energy = levels.loc[(atomic_number, ion_number, level_number)]["energy"] * u.eV
    energy = energy.to(u.Unit("cm-1"), equivalencies=u.spectral())
    assert_quantity_allclose(energy, exp_energy)


@with_test_db
@pytest.mark.parametrize("atomic_number, ion_number, level_number_lower, level_number_upper, exp_wavelength",[
    (7, 5, 1, 2, 1907.9000 * u.Unit("angstrom")),
    (4, 2, 0, 6, 10.0255 * u.Unit("angstrom"))
])
def test_create_lines(lines, atomic_number, ion_number,
                       level_number_lower, level_number_upper, exp_wavelength):
    lines = lines.set_index(["atomic_number", "ion_number",
                              "level_number_lower", "level_number_upper"])
    wavelength = lines.loc[(atomic_number, ion_number,
                                        level_number_lower, level_number_upper)]["wavelength"] * u.Unit("angstrom")
    assert_quantity_allclose(wavelength, exp_wavelength)


# ToDo: Implement real tests
@with_test_db
def test_create_collisions_df(collisions):
    assert True


@with_test_db
def test_create_macro_atom_df(macro_atom):
    assert True


@with_test_db
def test_create_macro_atom_ref_df(macro_atom_references):
    assert True


@with_test_db
def test_atom_data_to_hdf(atom_data, hdf5_path):
    atom_data.to_hdf(hdf5_path)