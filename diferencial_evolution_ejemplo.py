"""
ALGORITMO DE EVOLUCIÓN DIFERENCIAL (Differential Evolution)
============================================================

Ejemplo educativo implementado en Python
Autor: Ejemplo para universidad
Fecha: Octubre 2025

Este algoritmo es útil para optimizar funciones continuas y encontrar
mínimos o máximos globales.
"""

import numpy as np
import matplotlib.pyplot as plt


# ============================================================================
# FUNCIONES DE PRUEBA (Funciones objetivo a optimizar)
# ============================================================================

def funcion_esfera(x):
    """
    Función esfera: f(x) = sum(x_i^2)
    Mínimo global: f(0, 0, ..., 0) = 0
    Es una función convexa simple, ideal para empezar.
    """
    return np.sum(x**2)


def funcion_rastrigin(x):
    """
    Función de Rastrigin: función multimodal (muchos mínimos locales)
    Mínimo global: f(0, 0, ..., 0) = 0
    Es más difícil porque tiene muchos mínimos locales.
    """
    n = len(x)
    return 10*n + np.sum(x**2 - 10*np.cos(2*np.pi*x))


def funcion_rosenbrock(x):
    """
    Función de Rosenbrock: f(x) = sum(100*(x_{i+1} - x_i^2)^2 + (1-x_i)^2)
    Mínimo global: f(1, 1, ..., 1) = 0
    Tiene un valle estrecho, difícil de optimizar.
    """
    return np.sum(100.0 * (x[1:] - x[:-1]**2)**2 + (1 - x[:-1])**2)


# ============================================================================
# ALGORITMO DE EVOLUCIÓN DIFERENCIAL
# ============================================================================

class EvolucionDiferencial:
    """
    Implementación del algoritmo de Evolución Diferencial (DE)
    
    Parámetros:
    -----------
    funcion_objetivo : callable
        Función a minimizar
    limites : list of tuples
        Límites para cada dimensión [(min1, max1), (min2, max2), ...]
    tamaño_poblacion : int
        Número de individuos en la población (típicamente 10*D donde D=dimensiones)
    F : float
        Factor de mutación (típicamente entre 0.4 y 1.0)
    CR : float
        Probabilidad de cruce (típicamente entre 0.5 y 0.9)
    max_generaciones : int
        Número máximo de generaciones (iteraciones)
    """
    
    def __init__(self, funcion_objetivo, limites, tamaño_poblacion=50, 
                 F=0.8, CR=0.7, max_generaciones=100):
        self.funcion_objetivo = funcion_objetivo
        self.limites = np.array(limites)
        self.dimensiones = len(limites)
        self.tamaño_poblacion = tamaño_poblacion
        self.F = F  # Factor de mutación diferencial
        self.CR = CR  # Probabilidad de cruce
        self.max_generaciones = max_generaciones
        
        # Para almacenar resultados
        self.historial_mejor_fitness = []
        self.mejor_solucion = None
        self.mejor_fitness = np.inf
        
    def inicializar_poblacion(self):
        """
        Crea una población inicial aleatoria dentro de los límites especificados.
        Cada individuo es un vector de D dimensiones.
        """
        poblacion = np.random.rand(self.tamaño_poblacion, self.dimensiones)
        
        # Escalar los valores al rango especificado por los límites
        min_vals = self.limites[:, 0]
        max_vals = self.limites[:, 1]
        poblacion = min_vals + poblacion * (max_vals - min_vals)
        
        return poblacion
    
    def mutar(self, poblacion, indice_actual):
        """
        MUTACIÓN DIFERENCIAL
        ====================
        Estrategia DE/rand/1: v = x_r1 + F * (x_r2 - x_r3)
        
        Selecciona 3 individuos aleatorios diferentes y crea un vector mutante
        combinándolos con el factor de escala F.
        
        Parámetros:
        -----------
        poblacion : array
            Población actual
        indice_actual : int
            Índice del individuo actual (para no seleccionarlo)
            
        Returns:
        --------
        vector_mutante : array
            Nuevo vector creado por mutación diferencial
        """
        # Seleccionar 3 índices aleatorios diferentes entre sí y del actual
        indices = list(range(self.tamaño_poblacion))
        indices.remove(indice_actual)
        r1, r2, r3 = np.random.choice(indices, 3, replace=False)
        
        # Crear el vector mutante: v = x_r1 + F * (x_r2 - x_r3)
        vector_mutante = poblacion[r1] + self.F * (poblacion[r2] - poblacion[r3])
        
        # Asegurar que el vector mutante está dentro de los límites
        vector_mutante = np.clip(vector_mutante, self.limites[:, 0], self.limites[:, 1])
        
        return vector_mutante
    
    def cruzar(self, individuo_objetivo, vector_mutante):
        """
        CRUCE BINOMIAL
        ==============
        Combina el individuo actual con el vector mutante.
        Cada dimensión se toma del mutante con probabilidad CR,
        sino se toma del objetivo.
        
        Se garantiza que al menos una dimensión venga del mutante.
        
        Parámetros:
        -----------
        individuo_objetivo : array
            Individuo actual (padre)
        vector_mutante : array
            Vector creado por mutación
            
        Returns:
        --------
        individuo_trial : array
            Nuevo individuo candidato (hijo)
        """
        individuo_trial = np.copy(individuo_objetivo)
        
        # Generar máscara aleatoria para decidir qué genes tomar del mutante
        mascara_cruce = np.random.rand(self.dimensiones) < self.CR
        
        # Asegurar que al menos un gen venga del mutante
        if not np.any(mascara_cruce):
            mascara_cruce[np.random.randint(0, self.dimensiones)] = True
        
        # Aplicar el cruce
        individuo_trial[mascara_cruce] = vector_mutante[mascara_cruce]
        
        return individuo_trial
    
    def seleccionar(self, individuo_objetivo, individuo_trial):
        """
        SELECCIÓN
        =========
        Compara el hijo (trial) con el padre (objetivo).
        Si el hijo es mejor (menor fitness), reemplaza al padre.
        Esto es selección "codiciosa" (greedy).
        
        Parámetros:
        -----------
        individuo_objetivo : array
            Padre
        individuo_trial : array
            Hijo
            
        Returns:
        --------
        mejor_individuo : array
            El mejor entre padre e hijo
        mejor_fitness : float
            Fitness del mejor individuo
        """
        fitness_objetivo = self.funcion_objetivo(individuo_objetivo)
        fitness_trial = self.funcion_objetivo(individuo_trial)
        
        if fitness_trial <= fitness_objetivo:
            return individuo_trial, fitness_trial
        else:
            return individuo_objetivo, fitness_objetivo
    
    def optimizar(self, verbose=True):
        """
        EJECUTAR EL ALGORITMO COMPLETO
        ===============================
        
        Proceso:
        1. Inicializar población aleatoria
        2. Para cada generación:
           - Para cada individuo:
             a. Crear vector mutante
             b. Cruzar con el individuo actual
             c. Seleccionar el mejor
           - Registrar el mejor de la generación
        3. Retornar la mejor solución encontrada
        
        Parámetros:
        -----------
        verbose : bool
            Si True, imprime información durante la ejecución
            
        Returns:
        --------
        mejor_solucion : array
            Vector con la mejor solución encontrada
        mejor_fitness : float
            Valor de fitness de la mejor solución
        """
        # Paso 1: Inicializar población
        poblacion = self.inicializar_poblacion()
        
        if verbose:
            print("="*60)
            print("ALGORITMO DE EVOLUCIÓN DIFERENCIAL")
            print("="*60)
            print(f"Dimensiones: {self.dimensiones}")
            print(f"Tamaño de población: {self.tamaño_poblacion}")
            print(f"Factor de mutación (F): {self.F}")
            print(f"Probabilidad de cruce (CR): {self.CR}")
            print(f"Generaciones máximas: {self.max_generaciones}")
            print("="*60)
            print()
        
        # Paso 2: Evolución por generaciones
        for generacion in range(self.max_generaciones):
            # Nueva población para la siguiente generación
            nueva_poblacion = np.zeros_like(poblacion)
            
            # Para cada individuo en la población
            for i in range(self.tamaño_poblacion):
                # a) Mutación: crear vector mutante
                vector_mutante = self.mutar(poblacion, i)
                
                # b) Cruce: combinar individuo actual con mutante
                individuo_trial = self.cruzar(poblacion[i], vector_mutante)
                
                # c) Selección: mantener el mejor
                nueva_poblacion[i], fitness = self.seleccionar(poblacion[i], individuo_trial)
                
                # Actualizar el mejor global si encontramos uno mejor
                if fitness < self.mejor_fitness:
                    self.mejor_fitness = fitness
                    self.mejor_solucion = np.copy(nueva_poblacion[i])
            
            # Reemplazar la población antigua con la nueva
            poblacion = nueva_poblacion
            
            # Guardar el mejor fitness de esta generación
            self.historial_mejor_fitness.append(self.mejor_fitness)
            
            # Imprimir progreso cada 10 generaciones
            if verbose and (generacion % 10 == 0 or generacion == self.max_generaciones - 1):
                print(f"Generación {generacion:3d} | Mejor fitness: {self.mejor_fitness:.6e}")
        
        if verbose:
            print()
            print("="*60)
            print("OPTIMIZACIÓN COMPLETADA")
            print("="*60)
            print(f"Mejor solución encontrada: {self.mejor_solucion}")
            print(f"Valor de fitness: {self.mejor_fitness:.6e}")
            print("="*60)
        
        return self.mejor_solucion, self.mejor_fitness
    
    def graficar_convergencia(self):
        """
        Grafica cómo el mejor fitness mejora a lo largo de las generaciones.
        Esto muestra la convergencia del algoritmo.
        """
        plt.figure(figsize=(10, 6))
        plt.plot(self.historial_mejor_fitness, linewidth=2)
        plt.xlabel('Generación', fontsize=12)
        plt.ylabel('Mejor Fitness', fontsize=12)
        plt.title('Convergencia del Algoritmo de Evolución Diferencial', fontsize=14)
        plt.grid(True, alpha=0.3)
        plt.yscale('log')  # Escala logarítmica para ver mejor la convergencia
        plt.tight_layout()
        plt.show()


# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

def ejemplo_1_funcion_esfera():
    """
    Ejemplo 1: Optimizar la función esfera en 5 dimensiones
    Esta es una función simple, el algoritmo debería encontrar fácilmente el mínimo.
    """
    print("\n" + "="*60)
    print("EJEMPLO 1: Función Esfera (5D)")
    print("="*60)
    
    # Definir límites para cada dimensión: [-10, 10]
    dimensiones = 5
    limites = [(-10, 10) for _ in range(dimensiones)]
    
    # Crear instancia del algoritmo
    de = EvolucionDiferencial(
        funcion_objetivo=funcion_esfera,
        limites=limites,
        tamaño_poblacion=50,
        F=0.8,
        CR=0.7,
        max_generaciones=100
    )
    
    # Ejecutar optimización
    mejor_solucion, mejor_fitness = de.optimizar(verbose=True)
    
    # Mostrar gráfica de convergencia
    de.graficar_convergencia()
    
    return de


def ejemplo_2_funcion_rastrigin():
    """
    Ejemplo 2: Optimizar la función de Rastrigin en 10 dimensiones
    Esta función tiene muchos mínimos locales, es más desafiante.
    """
    print("\n" + "="*60)
    print("EJEMPLO 2: Función de Rastrigin (10D)")
    print("="*60)
    
    # Definir límites: [-5.12, 5.12] es el rango típico para Rastrigin
    dimensiones = 10
    limites = [(-5.12, 5.12) for _ in range(dimensiones)]
    
    # Crear instancia del algoritmo
    de = EvolucionDiferencial(
        funcion_objetivo=funcion_rastrigin,
        limites=limites,
        tamaño_poblacion=100,  # Más individuos para función más difícil
        F=0.8,
        CR=0.9,
        max_generaciones=200  # Más generaciones
    )
    
    # Ejecutar optimización
    mejor_solucion, mejor_fitness = de.optimizar(verbose=True)
    
    # Mostrar gráfica de convergencia
    de.graficar_convergencia()
    
    return de


def ejemplo_3_funcion_rosenbrock():
    """
    Ejemplo 3: Optimizar la función de Rosenbrock en 5 dimensiones
    Esta función tiene un valle estrecho y curvo, difícil de seguir.
    """
    print("\n" + "="*60)
    print("EJEMPLO 3: Función de Rosenbrock (5D)")
    print("="*60)
    
    # Definir límites: [-5, 10]
    dimensiones = 5
    limites = [(-5, 10) for _ in range(dimensiones)]
    
    # Crear instancia del algoritmo
    de = EvolucionDiferencial(
        funcion_objetivo=funcion_rosenbrock,
        limites=limites,
        tamaño_poblacion=75,
        F=0.8,
        CR=0.7,
        max_generaciones=300
    )
    
    # Ejecutar optimización
    mejor_solucion, mejor_fitness = de.optimizar(verbose=True)
    
    # Mostrar gráfica de convergencia
    de.graficar_convergencia()
    
    return de


def comparar_parametros():
    """
    Ejemplo 4: Comparar cómo diferentes parámetros afectan el rendimiento
    Esto es útil para entender la importancia de F y CR.
    """
    print("\n" + "="*60)
    print("EJEMPLO 4: Comparación de Parámetros")
    print("="*60)
    
    dimensiones = 5
    limites = [(-10, 10) for _ in range(dimensiones)]
    
    # Probar diferentes combinaciones de F y CR
    configuraciones = [
        {"F": 0.5, "CR": 0.5, "label": "F=0.5, CR=0.5"},
        {"F": 0.8, "CR": 0.7, "label": "F=0.8, CR=0.7"},
        {"F": 1.0, "CR": 0.9, "label": "F=1.0, CR=0.9"},
    ]
    
    plt.figure(figsize=(12, 6))
    
    for config in configuraciones:
        print(f"\nProbando configuración: {config['label']}")
        
        de = EvolucionDiferencial(
            funcion_objetivo=funcion_rastrigin,
            limites=limites,
            tamaño_poblacion=50,
            F=config["F"],
            CR=config["CR"],
            max_generaciones=100
        )
        
        de.optimizar(verbose=False)
        
        plt.plot(de.historial_mejor_fitness, label=config["label"], linewidth=2)
    
    plt.xlabel('Generación', fontsize=12)
    plt.ylabel('Mejor Fitness', fontsize=12)
    plt.title('Comparación de Parámetros F y CR', fontsize=14)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.yscale('log')
    plt.tight_layout()
    plt.show()


# ============================================================================
# EJECUCIÓN PRINCIPAL
# ============================================================================

if __name__ == "__main__":
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*10 + "ALGORITMO DE EVOLUCIÓN DIFERENCIAL" + " "*14 + "║")
    print("║" + " "*15 + "Ejemplos Educativos en Python" + " "*14 + "║")
    print("╚" + "="*58 + "╝")
    
    # Puedes ejecutar los ejemplos uno por uno o todos
    # Descomenta el que quieras probar:
    
    # Ejemplo básico (recomendado para empezar)
    de1 = ejemplo_1_funcion_esfera()
    
    # Ejemplo con función más compleja
    # de2 = ejemplo_2_funcion_rastrigin()
    
    # Ejemplo con función de valle estrecho
    # de3 = ejemplo_3_funcion_rosenbrock()
    
    # Comparar diferentes parámetros
    # comparar_parametros()
    
    print("\n" + "="*60)
    print("Programa finalizado exitosamente")
    print("="*60)

