from carsus import init_db
from carsus.io.nist import NISTWeightsCompIngester, NISTIonizationEnergiesIngester
from carsus.io.kurucz import GFALLIngester
from carsus.io.chianti_ import ChiantiIngester
from carsus.io.zeta import KnoxLongZetaIngester
from carsus.io.output import AtomData

# Init database
session = init_db()

# Basic atomic data
session.commit()

# Atomic weights (NIST)
weightscomp_ingester = NISTWeightsCompIngester(session)
weightscomp_ingester.ingest()
session.commit()

# Ionization energies and ground levels (NIST)
#ioniz_energies_ingester = NISTIonizationEnergiesIngester(session, spectra="Si")
#ioniz_energies_ingester.ingest(ionization_energies=True, ground_levels=True)
#session.commit()

# H-Zn levels and lines (Kurucz)
#gfall_ingester = GFALLIngester(session, fname="./docs/gfall.dat", ions="H-Zn")
#gfall_ingester.ingest(levels=True, lines=False)
#session.commit()

# Si I-II levels and lines (Chianti)
#chianti_ingester = ChiantiIngester(session, ions="Si 1-2")
#chianti_ingester.ingest(levels=True, lines=True)
#session.commit()

# Zeta data (Knox Long)
zeta_ingester = KnoxLongZetaIngester(session, './carsus/data/knox_long_recombination_zeta.dat')
zeta_ingester.ingest()
session.commit()

atom_data = AtomData(session, selected_atoms="Si", chianti_short_name='chianti_v9.0', chianti_ions="Si 1-2")z