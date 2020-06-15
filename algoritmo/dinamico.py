
import sys

# taken from: https://codereview.stackexchange.com/questions/1526/finding-all-k-subset-partitions
def subsets_k(collection, k):
    yield from partition_k(collection, k, k)


def partition_k(collection, min, k):
    if len(collection) == 1:
        yield [collection]
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


def dinamico(codigos_postales, cajas, n_destinos, t_caja, t_setup):

    def posibles_divisiones(lote):
        return list(subsets_k(list(lote.keys()), n_destinos))

    def calcular_tiempo(lote):
        return t_setup + sum(lote.values()) * t_caja

    def procesar_recursivo(lote):
        t_actual = calcular_tiempo(lote)
        divisiones = posibles_divisiones(lote)

        if len(divisiones) == 1:
            return t_actual

        t_min = sys.maxsize  # Valor muy grande
        for division in divisiones:
            t_division = 0
            for config in division:
                if len(config) > 1:
                    sub_lote = {k: lote[k] for k in config}
                    t_division += procesar_recursivo(sub_lote)
            if t_division < t_min:
                t_min = t_division
        return t_actual + t_min

    primer_lote = dict(zip(codigos_postales, cajas))
    primer_config = codigos_postales
    return procesar_recursivo(primer_lote)
