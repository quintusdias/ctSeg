import glob
import os
import pkg_resources as pkg
import sqlite3
import subprocess

import nibabel as nib


class CtSegDB(object):
    def __init__(self, root, dbase):
        """
        Parameters
        ----------
        root : str
            Root directory where Nifty files are expected to be found.
        dbase : str
            Path to output SQLITE3 database file.
        """
        self.conn = sqlite3.connect(dbase)
        self.cursor = self.conn.cursor()
        self.root = root

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def run(self):
        self.create_collection_table()
        self.create_team_table()
        self.create_base_image_table()
        self.create_challenge_table()

        self.populate()

    def create_team_table(self):
        sql = """
              DROP TABLE IF EXISTS team
              """
        self.cursor.execute(sql)

        sql = """
              CREATE TABLE team (
                  id            INTEGER PRIMARY KEY AUTOINCREMENT,
                  team          VARCHAR(30)
              )
              """
        self.cursor.execute(sql)

        self.cursor.execute("INSERT INTO team VALUES (NULL, 'cumc')")
        self.cursor.execute("INSERT INTO team VALUES (NULL, 'moffitt')")
        self.cursor.execute("INSERT INTO team VALUES (NULL, 'stanford')")

        self.conn.commit()

    def create_challenge_table(self):
        sql = """
              DROP TABLE IF EXISTS challenge
              """
        self.cursor.execute(sql)

        sql = """
              CREATE TABLE challenge (
                  id            INTEGER PRIMARY KEY AUTOINCREMENT,
                  base_image_id INTEGER,
                  team_id       INTEGER,
                  collection_id INTEGER,
                  label         TEXT,
                  run_id        INTEGER,
                  file          TEXT,
                  FOREIGN KEY(base_image_id) REFERENCES base_image(id),
                  FOREIGN KEY(team_id) REFERENCES team(id),
                  FOREIGN KEY(collection_id) REFERENCES collection(id)
              )
              """
        self.cursor.execute(sql)
        self.conn.commit()

    def create_base_image_table(self):
        sql = """
              DROP TABLE IF EXISTS base_image
              """
        self.cursor.execute(sql)

        sql = """
              CREATE TABLE base_image (
                  id            INTEGER PRIMARY KEY AUTOINCREMENT,
                  collection_id INTEGER,
                  label         TEXT,
                  file          TEXT,
                  FOREIGN KEY(collection_id) REFERENCES collection(id)
              )
              """
        self.cursor.execute(sql)

    def populate(self):
        collection_dirs = glob.glob(os.path.join(self.root, '*'))

        # Verify that the directory names are valid.
        sql1 = """
               SELECT id FROM collection
               WHERE name = ?
               """
        for collection in [os.path.basename(d) for d in collection_dirs]:
            self.cursor.execute(sql1, (collection,))
            results = self.cursor.fetchall()

            # The only directory entries here should be collection names.
            assert(len(results) == 1)

            collection_id = results[0][0]

            # Two items in the next directory level.  There may be nifty files,
            # soft-links, or directories.  The names of the directories are the
            # labels.  Corresponding to each label should be a nifty file
            # with the same name.  This may be a soft link or an actual file.
            items = glob.glob(os.path.join(self.root, collection, '*'))
            labels = [os.path.basename(item) for item in items if
                      os.path.isdir(item)]
            for label in labels:
                label_dir = os.path.join(self.root, collection, label)
                nifti = label_dir + '.nii'
                if not os.path.exists(nifti):
                    msg = "Expected NIFTI {} did not exist"
                    raise RuntimeError(msg.format(nifti))

                # Just store the path relative to the root.
                relfile = nifti[len(self.root) + 1:]
                sql2 = """
                       INSERT INTO base_image VALUES (NULL, ?, ?, ?)
                       """
                self.cursor.execute(sql2, (collection_id, label, relfile))

                # Get the base image ID back
                sql3 = """
                       SELECT id from base_image
                       WHERE file = ?
                       """
                self.cursor.execute(sql3, (relfile,))
                base_image_id = self.cursor.fetchone()[0]

                self.cursor.execute('SELECT * from team ORDER BY id')
                for team_id, team in self.cursor.fetchall():
                    path = os.path.join(self.root, collection, label,
                                        'alg{:02}_run*.nii.gz'.format(team_id))
                    lst = glob.glob(path)

                    for item in lst:

                        try:
                            img = nib.load(item)
                        except:
                            # If nibabel cannot open the item, it must not be
                            # a NIFTI, so skip it.
                            print('Could not load {}'.format(item))
                            continue

                        print('Successfully loaded {}'.format(item))
                        # Get the run ID.  This is brittle, should be
                        # replaced.
                        run_id = int(item[-8])

                        relfile = item[len(self.root) + 1:]
                        sql4 = """
                               INSERT INTO challenge VALUES
                               (NULL, ?, ?, ?, ?, ?, ?)
                               """
                        self.cursor.execute(sql4, (base_image_id, team_id,
                                                   collection_id, label,
                                                   run_id, relfile))

        self.conn.commit()

    def create_collection_table(self):
        sql = """
              DROP TABLE IF EXISTS collection
              """
        self.cursor.execute(sql)

        sql = """
              CREATE TABLE collection (
                  id   INTEGER PRIMARY KEY AUTOINCREMENT,
                  name VARCHAR(30)
              )
              """
        self.cursor.execute(sql)

        self.cursor.execute("INSERT INTO collection VALUES (NULL, 'cumc')")
        self.cursor.execute("INSERT INTO collection VALUES (NULL, 'lidc')")
        self.cursor.execute("INSERT INTO collection VALUES (NULL, 'moffitt')")
        self.cursor.execute("INSERT INTO collection VALUES (NULL, 'rider')")
        self.cursor.execute("INSERT INTO collection VALUES (NULL, 'stanford')")

        self.conn.commit()
