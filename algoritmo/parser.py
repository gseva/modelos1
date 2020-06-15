"""
Modulo que parsea archivos .dat

Cuidado: este parser utiliza ast.literal_eval para obtener las configuraciones,
que va a basicamente ejecutar cualquier código que se le pase.
"""

import ast, sys


def parse(filename):
    codigos, cajas, destinos, t_caja, t_setup, resultado = None, None, None, None, None, None
    with open(filename) as f:
        content = f.read()

        for statement in content.split(';'):
            if 'COD_POST = ' in statement:
                codigos = ast.literal_eval(statement.split('COD_POST = ')[-1])
            elif 'CAJAS = ' in statement:
                cajas = ast.literal_eval(statement.split('CAJAS = ')[-1])
            elif 'DESTINOS_POR_PASADA = ' in statement:
                destinos = ast.literal_eval(statement.split('DESTINOS_POR_PASADA = ')[-1])
            elif 'TIEMPO_PROC_CAJA = ' in statement:
                t_caja = ast.literal_eval(statement.split('TIEMPO_PROC_CAJA = ')[-1])
            elif 'TIEMPO_SETUP = ' in statement:
                t_setup = ast.literal_eval(statement.split('TIEMPO_SETUP = ')[-1])
            elif '/*Output:' in statement:
                for res in statement.split('\n'):
                    if 'Output' in res:
                        resultado = res
    return codigos, cajas, destinos, t_caja, t_setup, resultado


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Uso: parser.py archivo.dat')
    else:
        codigos, cajas, destinos, t_caja, t_setup, resultado = parse(sys.argv[1])
        print('Codigos:', codigos)
        print('Cajas:', cajas)
        print('Destinos:', destinos)
        print('Tiempo proc caja:', t_caja)
        print('Tiempo setup:', t_setup)
        print('Resultado esperado:', resultado)
