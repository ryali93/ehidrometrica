from criterio_accesibilidad import *
import subprocess
import math

if __name__ == '__main__':
    nrows = 100.0   # Cantidad de registros por iteracion
    params = get_parameters(ini=1)
    ngroups = int(math.ceil(len(params)/nrows))
    params_input = [','.join(list(i)) for i in zip(*[params[i:i+ngroups] for i in range(0, len(params), ngroups)])]
    filepy = os.path.join(BASE_DIR, 'criterio_accesibilidad.py')

    for index, value in enumerate(params_input, 1):
        try:
            print ('Subprocess nro: {}'.format(index))
            subprocess.call([filepy, value], shell=True)
        except Exception as e:
            print (e.message.__str__())
