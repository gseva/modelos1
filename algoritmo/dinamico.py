"""
Código del algoritmo de fuerza bruta/dinámico.
"""

import sys

# Cantidad máxima de códigos que puede procesar este algoritmo. Si la cantidad
# de códigos es mayor a este valor, el algoritmo va a aplicar una heuristica
# para separar los codigos en divisiones de igual tamaño para bajar la
# complejidad, y luego va a seguir con su procesamiento. Esto es necesario
# porque actualmente para el caso de 15 lotes el algoritmo no termina. Un valor
# que hace que termine para todos los casos es 12, pero el resultado deja de
# ser óptimo y es más parecido al resultado greedy.
MAX_CODIGOS = 999

# Algoritmo que devuelve todos los k-subsets posibles de un set de elementos
# Agarrado de: https://codereview.stackexchange.com/questions/1526/finding-all-k-subset-partitions
def subsets_k(collection, k):
    yield from partition_k(collection, k, k)

def partition_k(collection, min, k):
    if len(collection) == 1:
        yield [ collection ]
        return

    first = collection[0]
    for smaller in partition_k(collection[1:], min - 1, k):
        if len(smaller) > k: continue
        # insert `first` in each of the subpartition's subsets
        if len(smaller) >= min:
            for n, subset in enumerate(smaller):
                yield smaller[:n] + [[ first ] + subset]  + smaller[n+1:]
        # put `first` in its own subset
        if len(smaller) < k: yield [ [ first ] ] + smaller


def bucket_by_value(elements, k):
    """
    Separa el conjunto de elementos en k partes con la misma cantidad de
    elementos. El elemento se asigna a cada parte basado en su valor de mayor
    a menor.
    """
    result = [[] for _ in range(k)]
    items = reversed(sorted(elements.items(), key=lambda x: x[1]))
    for i, (el, _) in enumerate(items):
        result[i%k].append(el)
    return result


def dinamico(codigos_postales, cajas, n_destinos, t_caja, t_setup):
    config_times = {}
    subdivisiones_optimas = {}

    def posibles_divisiones(lote):
        return subsets_k(list(lote.keys()), n_destinos)

    def obtener_secuencia_optima(inicial):
        """
        Calcula la secuencia óptima a hacer dado una separación inicial. Se
        usa para mostrar el output
        """
        resultado = [subdivisiones_optimas[inicial]]
        for subdiv in subdivisiones_optimas[inicial]:
            if tuple(subdiv) in subdivisiones_optimas:
                resultado.extend(obtener_secuencia_optima(tuple(subdiv)))
        return resultado

    def calcular_tiempo(lote):
        return t_setup + sum(lote.values()) * t_caja

    def procesar_recursivo(lote):
        """ recursivamente calcula el funcional óptimo para el problema dado """
        t_actual = calcular_tiempo(lote)

        if len(lote) <= n_destinos:
            return t_actual

        if len(lote) > MAX_CODIGOS:
            # Heuristica para bajar la complejidad del algoritmo
            divisiones = [bucket_by_value(lote, n_destinos)]
        else:
            divisiones = posibles_divisiones(lote)

        t_min = sys.maxsize  # Valor muy grande
        division_optima = None
        for division in divisiones:
            t_division = 0
            for config in division:
                tup_config = tuple(config)
                if len(tup_config) > 1:
                    if tup_config not in config_times:
                        sub_lote = {k: lote[k] for k in tup_config}
                        config_times[tup_config] = procesar_recursivo(sub_lote)
                    t_division += config_times[tup_config]
            if t_division < t_min:
                t_min = t_division
                division_optima = division

        subdivisiones_optimas[tuple(lote.keys())] = division_optima
        return t_actual + t_min

    primer_lote = dict(zip(codigos_postales, cajas))

    for k, v in primer_lote.items():
        config_times[tuple(k)] = v

    primer_config = codigos_postales
    funcional = procesar_recursivo(primer_lote)
    secuencia_optima = obtener_secuencia_optima(tuple(codigos_postales))
    return funcional, secuencia_optima
