"""
EJEMPLO ULTRA SIMPLE Y VISUAL - Evolución Diferencial
======================================================

Este ejemplo muestra PASO A PASO qué hace el algoritmo.
Perfecto para entender exactamente cómo funciona.

PROBLEMA: Encontrar el valor de 'x' que hace x² lo más pequeño posible
RESPUESTA ESPERADA: x = 0 (porque 0² = 0)
"""

import random

# ============================================================
# CONFIGURACIÓN (puedes cambiar estos valores)
# ============================================================
poblacion_tamano = 5       # Solo 5 individuos para que sea fácil de seguir
F = 0.8                    # Factor de mutación (0.5-1.0 recomendado)
CR = 0.7                   # Probabilidad de cruce (0.5-0.9 recomendado)
generaciones = 20          # Solo 20 iteraciones

# Visualización detallada
MOSTRAR_DETALLE = True     # True = muestra paso a paso las primeras 2 generaciones
                           # False = solo muestra resumen cada 5 generaciones

# ============================================================
# FUNCIÓN A MINIMIZAR
# ============================================================
def funcion(x):
    """Queremos minimizar x²"""
    return x * x

# ============================================================
# PASO 1: CREAR POBLACIÓN INICIAL (números aleatorios)
# ============================================================
poblacion = []
for i in range(poblacion_tamano):
    x = random.uniform(-10, 10)  # Número aleatorio entre -10 y 10
    poblacion.append(x)

print()
print("╔" + "="*68 + "╗")
print("║" + " "*15 + "ALGORITMO DE EVOLUCIÓN DIFERENCIAL" + " "*19 + "║")
print("║" + " "*22 + "Ejemplo Ultra Simple" + " "*26 + "║")
print("╚" + "="*68 + "╝")
print()
print("📋 CONFIGURACIÓN:")
print(f"   • Población: {poblacion_tamano} individuos")
print(f"   • Factor F: {F} (controla tamaño de cambios)")
print(f"   • Probabilidad CR: {CR} (controla frecuencia de cambios)")
print(f"   • Generaciones: {generaciones}")
print(f"   • Objetivo: Minimizar f(x) = x²")
print()

print("="*70)
print("POBLACIÓN INICIAL (valores aleatorios):")
print("="*70)
mejor_inicial = min(poblacion, key=funcion)
for i, individuo in enumerate(poblacion):
    marca = "👑" if individuo == mejor_inicial else "  "
    print(f"{marca} Individuo {i+1}: x = {individuo:7.3f}  →  f(x) = {funcion(individuo):8.3f}")
print()
print(f"🎯 Mejor inicial: x = {mejor_inicial:7.3f}, f(x) = {funcion(mejor_inicial):8.3f}")
print()

# ============================================================
# PASO 2: EVOLUCIONAR (mejorar la población)
# ============================================================
mejoras_totales = 0

for gen in range(generaciones):
    
    # Mostrar header de generación si estamos en modo detalle
    if MOSTRAR_DETALLE and gen < 2:
        print("="*70)
        print(f"GENERACIÓN {gen+1} - Detalle paso a paso")
        print("="*70)
    
    # Para cada individuo
    for i in range(poblacion_tamano):
        
        # MUTACIÓN: Seleccionar 3 individuos aleatorios diferentes
        indices = [0, 1, 2, 3, 4]
        indices.remove(i)  # No puedo seleccionarme a mí mismo
        r1, r2, r3 = random.sample(indices, 3)
        
        # Mostrar detalle de mutación
        if MOSTRAR_DETALLE and gen < 2:
            print()
            print(f"┌─ Mejorando Individuo {i+1}: x = {poblacion[i]:6.3f}, f(x) = {funcion(poblacion[i]):7.3f}")
            print(f"│")
            print(f"│  🔀 MUTACIÓN: Seleccionados → Ind {r1+1}, Ind {r2+1}, Ind {r3+1}")
            print(f"│     x_r1 = {poblacion[r1]:6.3f}")
            print(f"│     x_r2 = {poblacion[r2]:6.3f}")
            print(f"│     x_r3 = {poblacion[r3]:6.3f}")
        
        # Crear individuo mutante: v = x_r1 + F * (x_r2 - x_r3)
        diferencia = poblacion[r2] - poblacion[r3]
        mutante = poblacion[r1] + F * diferencia
        
        if MOSTRAR_DETALLE and gen < 2:
            print(f"│")
            print(f"│     Diferencia = x_r2 - x_r3 = {diferencia:6.3f}")
            print(f"│     Mutante = {poblacion[r1]:6.3f} + {F} × {diferencia:6.3f} = {mutante:6.3f}")
        
        # Mantener dentro de límites [-10, 10]
        mutante_original = mutante
        if mutante < -10:
            mutante = -10
        if mutante > 10:
            mutante = 10
        
        if MOSTRAR_DETALLE and gen < 2 and mutante != mutante_original:
            print(f"│     ⚠️  Ajustado a límites: {mutante:6.3f}")
        
        # CRUCE: ¿Uso el mutante o mantengo el original?
        rand_cruce = random.random()
        if rand_cruce < CR:
            hijo = mutante
            decision_cruce = f"SÍ (rand={rand_cruce:.2f} < CR={CR})"
        else:
            hijo = poblacion[i]
            decision_cruce = f"NO (rand={rand_cruce:.2f} ≥ CR={CR})"
        
        if MOSTRAR_DETALLE and gen < 2:
            print(f"│")
            print(f"│  ⚔️  CRUCE: ¿Usar mutante? {decision_cruce}")
            print(f"│     Hijo = {hijo:6.3f}")
        
        # SELECCIÓN: Quedarme con el mejor
        fitness_padre = funcion(poblacion[i])
        fitness_hijo = funcion(hijo)
        
        if fitness_hijo < fitness_padre:
            if MOSTRAR_DETALLE and gen < 2:
                print(f"│")
                print(f"│  ✅ SELECCIÓN: Hijo es MEJOR")
                print(f"│     Padre: f({poblacion[i]:6.3f}) = {fitness_padre:7.3f}")
                print(f"│     Hijo:  f({hijo:6.3f}) = {fitness_hijo:7.3f}")
                print(f"│     → Reemplazamos con el hijo")
            poblacion[i] = hijo  # ¡Mejora! Lo guardo
            mejoras_totales += 1
            mejoro = "✓"
        else:
            if MOSTRAR_DETALLE and gen < 2:
                print(f"│")
                print(f"│  ❌ SELECCIÓN: Padre es MEJOR")
                print(f"│     Padre: f({poblacion[i]:6.3f}) = {fitness_padre:7.3f}")
                print(f"│     Hijo:  f({hijo:6.3f}) = {fitness_hijo:7.3f}")
                print(f"│     → Mantenemos el padre")
            mejoro = "✗"
        
        if MOSTRAR_DETALLE and gen < 2:
            print(f"└─ Resultado: Ind {i+1} = {poblacion[i]:6.3f}")
    
    # Mostrar progreso cada 5 generaciones (o siempre si es gen 0 o 1 en detalle)
    if (gen + 1) % 5 == 0 or (MOSTRAR_DETALLE and gen < 2):
        mejor = min(poblacion, key=funcion)
        if MOSTRAR_DETALLE and gen < 2:
            print()
            print("─" * 70)
        print(f"📊 Generación {gen+1:2d}: Mejor x = {mejor:7.4f}, f(x) = {funcion(mejor):8.6f}")
        if MOSTRAR_DETALLE and gen < 2:
            print()

# ============================================================
# PASO 3: MOSTRAR RESULTADO FINAL
# ============================================================
print()
print("="*70)
print("POBLACIÓN FINAL:")
print("="*70)
for i, individuo in enumerate(poblacion):
    mejoria = "⭐" if individuo == min(poblacion, key=funcion) else "  "
    print(f"{mejoria} Individuo {i+1}: x = {individuo:7.4f}  →  f(x) = {funcion(individuo):8.6f}")

mejor_solucion = min(poblacion, key=funcion)
peor_solucion = max(poblacion, key=funcion)
promedio = sum(poblacion) / len(poblacion)

print()
print("="*70)
print("🎯 RESULTADOS FINALES:")
print("="*70)
print(f"✅ Mejor x encontrado:  {mejor_solucion:8.6f}  →  f(x) = {funcion(mejor_solucion):.8f}")
print(f"❌ Peor x en población: {peor_solucion:8.6f}  →  f(x) = {funcion(peor_solucion):.8f}")
print(f"📊 Promedio población:  {promedio:8.6f}  →  f(x) = {funcion(promedio):.8f}")
print()
print(f"🎯 Óptimo teórico:       0.000000  →  f(x) = 0.00000000")
print(f"📏 Error absoluto:      {abs(mejor_solucion):.8f}")
print(f"📈 Mejoras realizadas:  {mejoras_totales} de {generaciones * poblacion_tamano} intentos ({mejoras_totales/(generaciones*poblacion_tamano)*100:.1f}%)")
print("="*70)

print()
print("💡 OBSERVACIONES:")
print("─" * 70)
print("• El algoritmo encontró una solución muy cercana al óptimo (x=0)")
print("• Cada generación mejoró o mantuvo la calidad de la población")
print("• La mutación diferencial usó las diferencias entre individuos")
print("• El cruce mantuvo diversidad en la población")
print("• La selección garantizó que nunca empeoráramos")
print("="*70)

