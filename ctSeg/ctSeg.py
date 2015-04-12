# -*- coding:  utf-8 -*-
import logging
import os
import pkg_resources as pkg
import re
import socket
import sqlite3
import subprocess
import sys
import tempfile

import numpy as np
from PyQt4 import QtCore, QtGui
import nibabel as nib
import skimage.measure
import scipy.misc

from .ctSeg_ui import Ui_Dialog


class CtSegForm(QtGui.QDialog):
    """
    Attributes
    ----------
    label : str
        Label identifying the base image currently active.  May be something
        like L0013.
    conn, cursor : database connection objects
        Handles database queries
    dataroot : str
        Path to where the base images and pairwise segmentations are stored.
    """
    def __init__(self, parent=None):
        """
        """
        if socket.gethostname() == 'nciphub':
            self.dataroot = '/data/groups/qinportal/ctSeg/resultsNii'
        else:
            self.dataroot = '/data/mgh/resultsNii'

        logging.basicConfig(format='%(message)s', level=logging.DEBUG)

        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.setup_c3d_environment()
        self.setup_database()

        self.setupCollectionTree()

        # When the execute button is pressed, initiate image processing.
        QtCore.QObject.connect(self.ui.executeButton,
                               QtCore.SIGNAL('clicked()'),
                               self.execute)

        # When the slider is changed, load a new slice.
        QtCore.QObject.connect(self.ui.imageSliceSlider,
                               QtCore.SIGNAL('sliderReleased()'),
                               self.load_new_slice)

    def load_new_slice(self):
        """
        When the slider is changed, we load a new slice.
        """
        slice_number = self.ui.imageSliceSlider.sliderPosition()
        self.display_image_slice(slice_number)

    def setup_database(self):
        """
        """
        relfile = os.path.join('share', 'moist_challenge.db')
        dbfile = pkg.resource_filename(__name__, relfile)
        self.conn = sqlite3.connect(dbfile)
        self.cursor = self.conn.cursor()

    def setup_c3d_environment(self):
        """
        Setup paths to be able to run C3D.
        """
        # Add some common paths to the c3d executable
        # First is on HubZero, 2nd is Mac with gui installation, 3rd is
        # MGH getafix.
        paths = ['/apps/share64/debian7/convert3d/nightly',
                 '/Applications/Convert3DGUI.app/Contents/bin',
                 '/space/getafix/1/users/jevans/c3d-1.0.0-Linux-x86_64/bin']

        env = dict(os.environ)
        env['PATH'] = os.environ['PATH']
        for path in paths:
            env['PATH'] = env['PATH'] + ':' + path
        self.env = env

    def run_c3d(self):
        """
        Drive c3d, obtain dice similarity coefficient between the two images.
        """
        # Want to match the output of the c3d command against the pattern
        # "Dice similarity coefficient:   \d*.\d*"
        #
        # Possibilities are any of the following:
        #     Dice similarity coefficient:   -nan
        #     Dice similarity coefficient:   1
        #     Dice similarity coefficient:   0.8243
        pattern = r"""Dice\ssimilarity\scoefficient:\s*
                      (?P<dice>-nan|\d(.\d*){0,1})"""
        regex = re.compile(pattern, re.VERBOSE)

        command = 'c3d -verbose {image1} {image2} -overlap 1'
        command = command.format(image1=self.image_1, image2=self.image_2)
        logging.info(command)
        self.c3d_output = command
        self.c3d_output += '\n'
        output = subprocess.check_output(command.split(' '), env=self.env)
        matchobj = regex.search(output.decode('utf-8'))
        logging.info(output)
        self.ui.diceLabel.setText(matchobj.group())
        return float(matchobj.group('dice'))

    def execute(self):
        """
        Call C3D, get the dice coefficient.
        """
        # What pairwise images were chosen?
        idx1 = self.ui.team1ComboBox.currentIndex()
        idx2 = self.ui.team2ComboBox.currentIndex()
        msg = "QT indices {} and {} chosen".format(idx1, idx2)
        logging.info(msg)

        qvar = self.ui.team1ComboBox.itemData(idx1, role=QtCore.Qt.UserRole)
        challenge_id1 = qvar
        qvar = self.ui.team1ComboBox.itemData(idx2, role=QtCore.Qt.UserRole)
        challenge_id2 = qvar

        if sys.hexversion < 0x03000000:
            challenge_id1 = challenge_id1.toString()
            challenge_id2 = challenge_id2.toString()

        msg = "Pairwise images {} and {} chosen"
        msg = msg.format(challenge_id1, challenge_id2)
        logging.info(msg)

        sql = """
              SELECT file FROM challenge
              WHERE id = :id
              """
        logging.info(sql)
        logging.info(type(challenge_id1))
        logging.info(str(challenge_id1))
        self.cursor.execute(sql, {'id': challenge_id1})

        row = self.cursor.fetchone()
        file1 = row[0]

        sql = """
              SELECT file FROM challenge
              WHERE id = :id
              """
        self.cursor.execute(sql, {'id': challenge_id2})
        logging.info(sql)
        logging.info(str(challenge_id2))

        row = self.cursor.fetchone()
        file2 = row[0]
        logging.info("file1 = {}".format(file1))
        logging.info("file2 = {}".format(file2))
        self.image_1 = os.path.join(self.dataroot, file1)
        self.image_2 = os.path.join(self.dataroot, file2)
        logging.info("loading {}".format(self.image_1))
        self.image1_data = nib.load(self.image_1).get_data()
        logging.info("loading {}".format(self.image_2))
        self.image2_data = nib.load(self.image_2).get_data()
        flt = self.run_c3d()

        self.setupBaseImage()

    def display_image_slice(self, slice_number):
        """

        Reference
        ---------
        scikit-image.org/docs/dev/auto_examples/plot_contours.html#example-plot-contours.py
        """
        height, width, depth = self.image_data.shape

        # Retrieve user image contours at the specified slice.
        slice1 = self.image1_data[:, :, slice_number]
        slice_contours_1 = skimage.measure.find_contours(slice1, 0.8)
        slice2 = self.image2_data[:, :, slice_number]
        slice_contours_2 = skimage.measure.find_contours(slice2, 0.8)

        image_slice = scipy.misc.bytescale(self.image_data[:, :, slice_number])
        faux_3d = np.zeros((height, width, 3))
        faux_3d[:, :, 0] = image_slice
        faux_3d[:, :, 1] = image_slice
        faux_3d[:, :, 2] = image_slice

        # Color user image 1 contours as red
        for contour in slice_contours_1:
            rows = contour[:, 0].round().astype(np.int32)
            cols = contour[:, 1].round().astype(np.int32)
            faux_3d[rows, cols, 0] = 0
            faux_3d[rows, cols, 1] = 0
            faux_3d[rows, cols, 2] = 255

        # Color user image 2 contours as green
        for contour in slice_contours_2:
            rows = contour[:, 0].round().astype(np.int32)
            cols = contour[:, 1].round().astype(np.int32)
            faux_3d[rows, cols, 0] = 0
            faux_3d[rows, cols, 1] = 255
            faux_3d[rows, cols, 2] = 0

        with tempfile.NamedTemporaryFile(suffix='.png') as tfile:
            scipy.misc.imsave(tfile.name, np.flipud(faux_3d.T))
            tfile.flush()

            qimage = QtGui.QImage(tfile.name)

        pixmap = QtGui.QPixmap(qimage)

        myScaledPixmap = pixmap.scaled(self.ui.graphicsView.size(),
                                       QtCore.Qt.KeepAspectRatio)
        self.scene.addPixmap(myScaledPixmap)
        self.scene.update()

    def setupBaseImage(self):
        """
        """
        sql = """
              SELECT file FROM base_image
              WHERE label = ?
              """
        self.cursor.execute(sql, (str(self.label),))
        row = self.cursor.fetchone()
        filepath = row[0]
        img = nib.load(os.path.join(self.dataroot, filepath))
        self.image_data = img.get_data()

        height, width, depth = self.image_data.shape

        # Set the slider range.  Allow the user to look thru all slices.
        self.ui.imageSliceSlider.setMinimum(0)
        self.ui.imageSliceSlider.setMaximum(depth-1)

        self.scene = QtGui.QGraphicsScene(self)
        self.ui.graphicsView.setScene(self.scene)

        self.display_image_slice(0)

    def setupCollectionTree(self):
        """
        Populate the collection/base image tree from the sqlite3 database.
        """
        self.ui.collectionTreeWidget.setColumnCount(2)
        self.ui.collectionTreeWidget.setHeaderLabels(['Collection',
                                                      'Base Image'])
        QtCore.QObject.connect(
            self.ui.collectionTreeWidget,
            QtCore.SIGNAL('itemClicked(QTreeWidgetItem*, int)'),
            self.treeItemClicked
        )

        # setup the top level items.  These are just the collection names.
        sql = """
              SELECT id, name from collection
              """
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        for id, collection_name in rows:

            branch = QtGui.QTreeWidgetItem(self.ui.collectionTreeWidget)
            branch.setText(0, collection_name)

            # Get the base images for the collection.
            sql = """
                  SELECT base_image.id, base_image.file, base_image.label
                  FROM base_image
                  INNER JOIN collection
                      ON base_image.collection_id = collection.id
                  WHERE collection.name = :collection_name
                  """
            logging.info(sql)
            self.cursor.execute(sql, {'collection_name': collection_name})
            base_image_rows = self.cursor.fetchall()
            for base_image_id, base_image_relpath, label in base_image_rows:
                leaf = QtGui.QTreeWidgetItem(branch)
                leaf.setText(1, label)
                # leaf.setData(1, QtCore.Qt.UserRole, QtCore.QVariant(label))
                leaf.setData(1, QtCore.Qt.UserRole, label)

            branch.setExpanded(False)

    def treeItemClicked(self, leaf, column):
        """
        A base image was chosen.  Retrieve the base image id from the widget
        and retrieve the runs associated with that image.
        """
        # Clear both combo boxes.
        self.ui.team1ComboBox.clear()
        self.ui.team2ComboBox.clear()

        label = leaf.data(column, QtCore.Qt.UserRole)
        if sys.hexversion < 0x03000000:
            label = label.toString()
        logging.info("Base image id = {0}".format(label))
        self.label = label

        # Get the runs associated with the base image and populate the combo
        # boxes.
        sql = """
              SELECT c.id, t.team, c.run_id
              FROM challenge c INNER JOIN team t on t.id = c.team_id
              WHERE label = :label
              """
        logging.info("sql:  {}".format(sql))
        logging.info("label:  {}".format(label))
        self.cursor.execute(sql, {'label': str(label)})
        rows = self.cursor.fetchall()
        for challenge_id, team, run_id in rows:
            name = "{0}-{1}".format(team, run_id)
            self.ui.team1ComboBox.addItem(name, userData=str(challenge_id))
            self.ui.team2ComboBox.addItem(name, userData=str(challenge_id))
