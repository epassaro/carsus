from carsus import init_db
from carsus.io.nist import NISTWeightsCompIngester, NISTIonizationEnergiesIngester
from carsus.io.kurucz import GFALLIngester

from carsus.model import Atom

session = init_db()

# Basic atomic data
session.commit()

# Atomic weights (NIST)
weightscomp_ingester = NISTWeightsCompIngester(session)
weightscomp_ingester.ingest()
session.commit()

# Ionization energies and ground levels (NIST)
ioniz_energies_ingester = NISTIonizationEnergiesIngester(session, spectra="Si")
ioniz_energies_ingester.ingest(ionization_energies=True, ground_levels=True)
session.commit()

# Levels and lines (Kurucz)
#gfall_ingester = GFALLIngester(session, fname="./gfall.dat", ions="Si 1-2")
#gfall_ingester.ingest(levels=True, lines=False)
#session.commit()