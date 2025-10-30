"""
EJEMPLO RÁPIDO - Algoritmo de Evolución Diferencial
====================================================
Este es un ejemplo minimalista para ejecutar inmediatamente
"""

import numpy as np
import matplotlib.pyplot as plt

# Semilla para resultados reproducibles (misma población inicial cada corrida)
np.random.seed(42)

# Función objetivo: minimizar x^2 + y^2 (un paraboloide)
def funcion_objetivo(x):
    """El mínimo está en (0, 0) con valor 0"""
    return x[0]**2 + x[1]**2

# Parámetros del algoritmo
NP = 20          # Tamaño de población
F = 0.8          # Factor de mutación
CR = 0.7         # Probabilidad de cruce
generaciones = 50  # Número de iteraciones
limites = [(-10, 10), (-10, 10)]  # Rango de búsqueda para x e y

# Inicializar población aleatoria
poblacion = np.random.uniform(-10, 10, (NP, 2))
mejor_fitness_historico = []

print("Iniciando optimización (Evolución Diferencial)...")
print("-" * 50)

# Mostrar población inicial
print("Población inicial (x1, x2):")
for i, ind in enumerate(poblacion):
    print(f"  Ind {i+1:02d}: ({ind[0]:.3f}, {ind[1]:.3f})")
print("-" * 50)

# Algoritmo principal
for gen in range(generaciones):
    for i in range(NP):
        # 1. MUTACIÓN: Seleccionar 3 individuos aleatorios
        indices = [idx for idx in range(NP) if idx != i]
        r1, r2, r3 = np.random.choice(indices, 3, replace=False)
        
        # Crear vector mutante
        mutante = poblacion[r1] + F * (poblacion[r2] - poblacion[r3])
        mutante = np.clip(mutante, -10, 10)  # Mantener dentro de límites
        
        # 2. CRUCE: Combinar individuo actual con mutante
        trial = np.copy(poblacion[i])
        for j in range(2):  # Para cada dimensión (x, y)
            if np.random.rand() < CR:
                trial[j] = mutante[j]
        
        # 3. SELECCIÓN: Mantener el mejor
        if funcion_objetivo(trial) < funcion_objetivo(poblacion[i]):
            poblacion[i] = trial
    
    # Encontrar y guardar el mejor de la generación
    fitness_poblacion = [funcion_objetivo(ind) for ind in poblacion]
    mejor_fitness = min(fitness_poblacion)
    mejor_fitness_historico.append(mejor_fitness)
    
    if gen % 10 == 0:
        mejor_idx = np.argmin(fitness_poblacion)
        mejor_sol = poblacion[mejor_idx]
        # Mensaje más pedagógico en términos de la planilla
        # "Generación" ≈ iteración del proceso evolutivo
        # "f(x)" ≈ valor de la función objetivo del mejor individuo
        print(
            f"Generación {gen:2d} | Mejor f(x) = {mejor_fitness:.6f} | Mejor individuo (x1,x2) = ({mejor_sol[0]:.3f}, {mejor_sol[1]:.3f})"
        )

# Resultado final
fitness_final = [funcion_objetivo(ind) for ind in poblacion]
mejor_idx = np.argmin(fitness_final)
mejor_solucion = poblacion[mejor_idx]
mejor_valor = fitness_final[mejor_idx]

print("-" * 50)
print("🎯 RESUMEN FINAL")
print(f"   Mejor individuo encontrado (x1, x2) = ({mejor_solucion[0]:.6f}, {mejor_solucion[1]:.6f})")
print(f"   Mejor valor de la función f(x)      = {mejor_valor:.6f}")
print(f"   Óptimo teórico: (0, 0) → f(x)=0")

# Graficar convergencia
plt.figure(figsize=(10, 5))

# Gráfica 1: Convergencia
plt.subplot(1, 2, 1)
plt.plot(mejor_fitness_historico, 'b-', linewidth=2)
plt.xlabel('Generación')
plt.ylabel('Mejor f(x)')
plt.title('Convergencia de f(x) (menor es mejor)')
plt.grid(True, alpha=0.3)
plt.yscale('log')

# Gráfica 2: Población final sobre el contorno de la función
plt.subplot(1, 2, 2)
x = np.linspace(-10, 10, 100)
y = np.linspace(-10, 10, 100)
X, Y = np.meshgrid(x, y)
Z = X**2 + Y**2
plt.contour(X, Y, Z, levels=20, alpha=0.6)
plt.scatter(poblacion[:, 0], poblacion[:, 1], c='red', s=50, alpha=0.6, label='Población (individuos)')
plt.scatter(mejor_solucion[0], mejor_solucion[1], c='green', s=200, marker='*', 
            label='Mejor individuo', edgecolors='black', linewidths=2)
plt.scatter(0, 0, c='blue', s=100, marker='x', label='Óptimo real', linewidths=3)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Población Final')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("\n✅ Ejecución completada exitosamente!")

