
import sys
import time

from parser import parse
from greedy_sol import GreedySol


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Uso: run.py archivo.dat')
    else:
        codigos, cajas, destinos, t_caja, t_setup, resultado = parse(sys.argv[1])
        print('***'*5, 'Configuración:', '***'*5)
        print('Codigos:', codigos)
        print('Cajas:', cajas)
        print('Destinos:', destinos)
        print('Tiempo proc caja:', t_caja)
        print('Tiempo setup:', t_setup)
        print('Resultado esperado:', resultado)

        print('\n'+('***'*5), 'Ejecución', '***'*5)
        start_time = time.time()
        sol = GreedySol(t_caja, t_setup)
        sol.run(list(zip(codigos, cajas)), destinos)
        sol.results()

        print('\n'+('***'*10))
        print('Tiempo de ejecución: {} segundos'.format(time.time() - start_time))
