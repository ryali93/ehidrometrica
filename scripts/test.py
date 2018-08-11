from config.settings import *
import arcpy
import shutil
import threading

idrc = 'IDRC'

matrix = [i for i in os.listdir(MATRIX_DIR) if 'matrix' in i]

cuenca_por_region = [i[0] for i in arcpy.da.SearchCursor(EHIDROMETRICA, [idrc], "%s IS NOT NULL" % idrc, None, False,
                                                         (None, "GROUP BY %s" % idrc))]


def create_folder(name):
    path = os.path.join(MATRIX_DIR, name)
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)
    return path


def copy_files(path, files):
    for i in files:
        f = os.path.join(MATRIX_DIR, i)
        shutil.copy2(f, path)


def process(name):
    path = create_folder(name)
    files = filter(lambda x: i in x, matrix)
    copy_files(path, files)


for i in cuenca_por_region:
    print i
    try:
        t = threading.Thread(target=process, args=(i,))
        t.start()
        t.join()
    except Exception as e:
        print e.message
