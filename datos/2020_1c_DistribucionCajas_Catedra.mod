/*********************************************
 * OPL 12.9.0.0 Model
 * Author: LaCatedra
 * Creation Date: Mar 02, 2020 at 16:00:07
 *********************************************/
 
//Datos de entrada
{string} COD_POST = ...;
int CAJAS[COD_POST] = ...;
int DESTINOS_POR_PASADA = ...;
int TIEMPO_PROC_CAJA = ...;
int TIEMPO_SETUP = ...;

//Constantes
int M = 99999999;
float m = 0.0001;

int DPP = DESTINOS_POR_PASADA;

//Para la sumatoria y obtener la cantidad de nodos totales
int cantCodPost = card(COD_POST);

int NIVELES_ARBOL = ftoi(ceil((cantCodPost - 1) / (DPP - 1)));

int CANT_NODOS = ftoi((sum(i in 1..NIVELES_ARBOL) pow(DPP, i)) + 1);


range rangoNodos = 0..CANT_NODOS-1;

//Dado que no se puede extraer de la fórmula los nodos de la última pasada, utilizamos una cuenta
//auxiliar
float aux = (((DPP - 1) * CANT_NODOS) + 1)/ DPP;
int cantNodosUltNivel = ftoi(aux);

int indIniUltNivelNodos = CANT_NODOS-cantNodosUltNivel;
range rangoUltNivelNodos = indIniUltNivelNodos..CANT_NODOS-1;

//Para calcular los hijos, siendo 'ni' el indice del nodo y 'k' los dpp, usamos:
// (ni*k)+1,......(ni*k)+k
// y para calcular el padre del indice 'ni':
// floor((ni-1)/k)

range rangoPadres = 0..indIniUltNivelNodos-1;


//Variables del problema
dvar int Codigos[rangoNodos]; //Cant de codigos postales distintos que hay en un nodo
dvar boolean YMata[rangoNodos]; //1: si en el nodo se mata un codigo postal; 0: sino
dvar boolean Existe[COD_POST][rangoNodos];
dvar boolean TieneCodigos[rangoNodos]; //1: si en el nodo hay algun codigo; 0: en caso que no haya ninguno
dvar boolean YMatado[COD_POST][rangoNodos]; //1: si el codigo se mato en el nodo; 0: sino
dvar boolean YSetup[rangoNodos]; //1: si el nodo requiere setup (al tener mas de 1 codigo); 0 si no (el nodo tiene 1 cod o ninguno)

minimize
  //Tiempo Procesamiento cajas
  (sum(cod in COD_POST, nodo in rangoNodos) TIEMPO_PROC_CAJA *CAJAS[cod] * Existe[cod][nodo])-
  (sum(cod in COD_POST) TIEMPO_PROC_CAJA * CAJAS[cod]) +
  //Tiempo Set up scanner
  (sum(nodo in rangoNodos) TIEMPO_SETUP * YSetup[nodo]);

subject to {
	
	//Restricciones 1: Relacion Padre-Hijos #Codigos: 
	forall(nodo in rangoPadres) { 
		
		// Si se mata padre, los hijos no tienen codigos
		Restriccion1aPadreHijos:
		(sum(hijo in (nodo*DPP)+1..(nodo*DPP)+DPP) Codigos[hijo]) <= (1 - YMata[nodo]) * M;
		// Si no se mata padre, los codigos pasan a los hijos
		Restriccion1bPadreHijos:
		Codigos[nodo] - M * YMata[nodo] <=  (sum(hijo in (nodo*DPP)+1..(nodo*DPP)+DPP) Codigos[hijo]);
											(sum(hijo in (nodo*DPP)+1..(nodo*DPP)+DPP) Codigos[hijo]) <= Codigos[nodo] + YMata[nodo] * M;	
	}
	
	//Restricciones 2: // Todos los codigos existen en el primer nodo (nodo 0)
	forall(cod in COD_POST) {
		
		Restriccion2PrimerNodo: Existe[cod][0] == 1;
	}
	
	//Restricciones 3: Nodos-Codigos + Setup 
	forall(nodo in rangoNodos) {
		// Relacion entre Codigos[nodo] y la bivalente YMata[nodo]

		// |Codigos[nodo]|YMata[nodo]|
		// |-------------|-----------|
		// |      0      |     0     |
		// |      1      |     1     |
		// |     >1      |     0     |
		// |-------------------------|

		// para lograr esto se usa TieneCodigos[nodo]
		// |Codigos[nodo]|TieneCodigos[nodo]|
		// |-------------|------------------|
		// |      0      |        0         |
		// |     >0      |        1         |
		// |--------------------------------|

		// Si no hay codigos en nodo, la bivalente TieneCodigos vale 0
		Restriccion3aTieneCodigos:
		TieneCodigos[nodo] <= Codigos[nodo];
		// Si hay codigos en nodo, la bivalente TieneCodigos vale 1
		Restriccion3bTieneCodigos:
		m * Codigos[nodo] <= TieneCodigos[nodo];
		
		// Si tiene solo 1 codigo, se mata		
		Restriccion3cTieneCodigos:
		-M * (1 - TieneCodigos[nodo]) + (1 - YMata[nodo]) <= Codigos[nodo] -1;
		// Si tiene mas de 1 codigo, no se mata
		Restriccion3dTieneCodigos:
		m * (Codigos[nodo] - 1) <= (1 - YMata[nodo]) + M * (1 - TieneCodigos[nodo]);
		// Si no tiene codigos, no se mata
		Restriccion3eTieneCodigos:
		1 - TieneCodigos[nodo] <= (1 - YMata[nodo]);	
	
		//Sumatoria de codigos en cada nodo
		Restriccion3fSumCodigos: (sum(cod in COD_POST) Existe[cod][nodo]) == Codigos[nodo];
		
		
		//------------------- SETUP -----------------
			
		// |Codigos[nodo]|YSetup[nodo]|
		// |-------------|-----------|
		// |      0      |     0     |
		// |      1      |     0     |
		// |     >1      |     1     |
		// |-------------------------|
		// Si no hay codigos en nodo, la bivalente YSetup vale 0
		Restriccion3gSetup:
		YSetup[nodo] <= Codigos[nodo];
		// Si hay 1 codigo en nodo, la bivalente YSetup vale 0 (el funcional tira para abajo)
		// Si hay >1 codigos en nodo, la bivalente YSetup vale 1
		Restriccion3hSetup:
		m * (Codigos[nodo] - 1) <= YSetup[nodo];
		
			
	}
	
	//Restricciones 4: Relacion Padre-Hijos Existencia Codigos:
	forall(padre in rangoPadres) {
		forall(cod in COD_POST) {
				
			// Si se mata padre, los hijos no tienen codigos
			Restriccion4aMataPadre:
			(sum(hijo in (padre*DPP)+1..(padre*DPP)+DPP) Existe[cod][hijo]) <= (1 -YMata[padre]) * M;
			// Si no se mata padre y tiene codigo, el codigo pasa a algun hijo  
			Restriccion4bMataPadre:
														 					   Existe[cod][padre] - M * YMata[padre] <= (sum(hijo in (padre*DPP)+1..(padre*DPP)+DPP) Existe[cod][hijo]);
			// Si no se mata padre y no tiene codigo, los hijos tampoco tienen codigos 
			Restriccion4cMataPadre:
			(sum(hijo in (padre*DPP)+1..(padre*DPP)+DPP) Existe[cod][hijo]) <= Existe[cod][padre] + YMata[padre] * M;		
		}
	}
	
	//Restricciones 5: En el ultimo nivel no puede haber mas de 1 codigo en cada nodo
	forall(nodo in rangoUltNivelNodos) {
		Restriccion5UltNivel: Codigos[nodo] <= 1;	
	}
	
	//Restricciones 6: Hermanos
	forall(nodo in 1..CANT_NODOS-2) {
		if (floor((nodo-1)/DPP) == floor((nodo)/DPP)) { //Esto es si tienen el mismo padre
			//Completamos de derecha a izquierda los hermanos
			Restriccion6Hermanos: Codigos[nodo] <= Codigos[nodo+1];		
		}
	}	
	
	//Restricciones 7: Saber en que nodo se mata cada codigo postal
	forall(cod in COD_POST) {
		forall(nodo in rangoNodos) {
				
			Restriccion7aNodoMataCod:
			2 * YMatado[cod][nodo] <= 	Existe[cod][nodo] + YMata[nodo];
			
			Restriccion7bNodoMataCod:
										Existe[cod][nodo] + YMata[nodo] <= YMatado[cod][nodo] + 1;
		}
	}
	
}
