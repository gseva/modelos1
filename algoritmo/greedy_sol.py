import sys
from heapq import heapreplace

# --- Datos de prueba 

CAJAS_X_CODPOST = [
	('A', 10),
	('B', 10),
	('C', 10),
	('D', 10),
	('E', 10),
	('F', 10),
	('G', 10),
	('H', 10),
	('I', 10),
	('J', 10),
	('K', 10),
	('L', 10),
	('M', 10),
	('N', 10),
	('O', 10),
	('P', 10),
	('Q', 10),
	('R', 10)
]

DEST_PASADA = 4
TIEMPO_PROC_CAJA = 1
TIEMPO_SETUP = 0



# --- Solucion

P_CP = 0	# Index consts
P_CJ = 1

class GreedySol():

	def __init__(self, tproc, tsetup, debug_mode=True):
		self.MATADO_X_RONDA = {}
		self.FUNCIONAL = 0
		self.tproc = tproc
		self.tsetup = tsetup
		self.debug = debug_mode


	def run(self, cajas_cps, dests, nivel=0):
		self.MATADO_X_RONDA[nivel] = self.MATADO_X_RONDA.get(nivel, [])
		self.FUNCIONAL+=self.tsetup 									# Sumo tiempo de setup al iniciar nivel
		cajas_cps.sort(key= lambda x: x[1], reverse=True)				# Ordenar CPs por cantidad de cajas de mayor a menor

		buckets_dest = [[] for i in range(dests)]						# Crea tantos buckets como cantidad de destinos haya
		heap_cajas_dest = [(0,i) for i in range(dests)]					# Heap de minimos, para saber siempre cual es el bucket con menos cajas

		cant_cajas_proc = 0
		for cp in cajas_cps:											# Por cada CP (ordenados) los inserto en el bucket de destinos, 
			cant_cajas_proc+=cp[P_CJ]									# que menor cantidad de cajas tenga hasta el momento
			min_buck = heap_cajas_dest[0]
			buckets_dest[min_buck[1]].append(cp)
			updt_buck = (min_buck[0] + cp[P_CJ], min_buck[1])
			heapreplace(heap_cajas_dest, updt_buck)

		self.FUNCIONAL+=(cant_cajas_proc*self.tproc)					# Sumo el total de tiempo de procesamiento por cajas

		if (self.debug):
			self.step_printer(cajas_cps, buckets_dest, nivel)

		ronda_i = []
		for buck in buckets_dest:										# Por cada bucket, se ve su cantidad:
			if len(buck) == 0: continue									# 	Si no tiene elementos, no hace nada
			if len(buck) == 1:											#	Si tiene 1 elemento, lo añade como matado en la ronda
				ronda_i.append(buck[0][P_CP])
			else:														#	Si tiene >1 elementos, vuelve a correr el scanner
				self.run(buck, dests, nivel+1)

		self.MATADO_X_RONDA[nivel].append(ronda_i)						# Añade subset de nivel

	def step_printer(self, cajas_cps, buckets, nivel):
		indent_nivel = " " * 6 * nivel
		cps = [x[0] for x in cajas_cps] 
		bucks_cps = [[y[0] for y in x] for x in buckets] 
		print("{0}{1: >2}: Entrada={2}".format(indent_nivel, nivel, cps))
		print("{0}    Salidas={1}".format(indent_nivel, bucks_cps))

	def results(self):
		print("---- RESULTADOS DE CORRIDA ----")
		print("  Funcional =", self.FUNCIONAL)
		print("  Matados por ronda =",self.MATADO_X_RONDA)



# --- Corrida y resultados

if __name__ == '__main__':
	sol1 = GreedySol(TIEMPO_PROC_CAJA, TIEMPO_SETUP)
	sol1.run(CAJAS_X_CODPOST, DEST_PASADA)
	sol1.results()

