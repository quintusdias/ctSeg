import argparse
import sys

from PyQt4 import QtGui

from .ctSeg import CtSegForm
from .ctSegDB import CtSegDB


def run_ctseg():
    """
    Entry point for running the NCIPHUB application
    """
    app = QtGui.QApplication(sys.argv)
    myapp = CtSegForm()
    myapp.show()
    sys.exit(app.exec_())


def make_db():
    """
    Entry point for creating the SQLITE3 database.
    """
    description = 'Create moist challenge database'
    parser = argparse.ArgumentParser(description=description)

    msg = 'Data root of base images and pairwise segmentations'
    parser.add_argument('root', help=msg)

    msg = 'Output database'
    parser.add_argument('database', help=msg)

    args = parser.parse_args()
    o = CtSegDB(args.root, args.database)
    o.run()
