
import sys
import time

from parser import parse
from greedy_sol import GreedySol
from dinamico import dinamico


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(('Uso: run.py archivo.dat <algoritmo>\n\n'
               'Algoritmos disponibles: greedy/dinamico, por defecto: greedy'))
    else:
        codigos, cajas, destinos, t_caja, t_setup, resultado = parse(sys.argv[1])
        print('***'*5, 'Configuración:', '***'*5)
        print('Codigos:', codigos)
        print('Cajas:', cajas)
        print('Destinos:', destinos)
        print('Tiempo proc caja:', t_caja)
        print('Tiempo setup:', t_setup)
        print('Resultado esperado:', resultado)

        algoritmo = sys.argv[2] if len(sys.argv) > 2 else 'greedy'
        print('Algoritmo:', algoritmo)

        print('\n'+('***'*5), 'Ejecución', '***'*5)
        if algoritmo == 'greedy':
            start_time = time.time()
            sol = GreedySol(t_caja, t_setup)
            sol.run(list(zip(codigos, cajas)), destinos)
            end_time = time.time() - start_time
            sol.results()
        elif algoritmo == 'dinamico':
            start_time = time.time()
            resultado, secuencia = dinamico(codigos, cajas, destinos, t_caja, t_setup)
            end_time = time.time() - start_time
            print('Funcional:', resultado)
            print('Secuencia (excluyendo las triviales):')
            for division in secuencia:
                print(division)
        else:
            print('No existe el algoritmo', algoritmo)
            print('Opciones disponibles: greedy/dinamico')
            exit()
        print('\n'+('***'*10))
        print('Tiempo de ejecución: {:.5f} segundos'.format(end_time, ))
