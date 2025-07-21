from carsus import init_db
from carsus.io.nist import NISTWeightsCompIngester, NISTIonizationEnergiesIngester
from carsus.io.kurucz import GFALLIngester
from carsus.io.chianti_ import ChiantiIngester
from carsus.io.zeta import KnoxLongZetaIngester
from carsus.io.output import AtomData


REV = "2018"
IONS = "H-Zn"
IONS_CH = "H-He"
CH_VER = "8.0.2"
HDF5_OUTPUT = "kurucz_{0}_chianti_{1}_{2}_sql.h5".format(IONS, IONS_CH, REV)

# Init database
session = init_db()

# Basic atomic data
session.commit()

# Atomic weights (NIST)
weightscomp_ingester = NISTWeightsCompIngester(session)
weightscomp_ingester.ingest()
session.commit()

# Ionization energies and ground levels (NIST)
ioniz_energies_ingester = NISTIonizationEnergiesIngester(session, spectra=IONS)
ioniz_energies_ingester.ingest(ionization_energies=True, ground_levels=True)
session.commit()

# H-Zn levels and lines (Kurucz)
gfall_ingester = GFALLIngester(session, fname="./gfall.dat", ions=IONS)
gfall_ingester.ingest(levels=True, lines=True)
session.commit()

# Si I-II levels and lines (Chianti)
chianti_ingester = ChiantiIngester(session, ions=IONS_CH)
chianti_ingester.ingest(levels=True, lines=True, collisions=True)
session.commit()

# Zeta data (Knox Long)
zeta_ingester = KnoxLongZetaIngester(session, './carsus/data/knox_long_recombination_zeta.dat')
zeta_ingester.ingest()
session.commit()

# Create HDF5 file
atom_data = AtomData(session, 
                     selected_atoms=IONS,
                     chianti_short_name='chianti_v{0}'.format(CH_VER), 
                     chianti_ions=IONS_CH
                     )

atom_data.to_hdf(HDF5_OUTPUT, 
                 store_atom_masses=True, 
                 store_ionization_energies=True, 
                 store_levels=True, 
                 store_lines=True,
                 store_collisions=True,
                 store_macro_atom=True,
                 store_zeta_data=True
                 )
