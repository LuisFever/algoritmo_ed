"""
APLICACIÓN PRÁCTICA - Ajuste de Curvas con Evolución Diferencial
=================================================================

Este ejemplo muestra cómo usar DE para resolver un problema real:
Ajustar una función a datos experimentales (regresión no lineal)

Problema: Tenemos datos de temperatura vs tiempo y queremos encontrar
los parámetros de un modelo de enfriamiento de Newton:
T(t) = T_ambiente + (T_inicial - T_ambiente) * exp(-k*t)
"""

import numpy as np
import matplotlib.pyplot as plt
from diferencial_evolution_ejemplo import EvolucionDiferencial


# ============================================================================
# GENERAR DATOS SINTÉTICOS (simulando datos experimentales)
# ============================================================================

def generar_datos_experimentales():
    """
    Simula datos de enfriamiento de un objeto.
    Modelo real: T(t) = 20 + 80*exp(-0.1*t)
    """
    # Parámetros reales (que queremos recuperar)
    T_amb_real = 20      # Temperatura ambiente (°C)
    T_ini_real = 100     # Temperatura inicial (°C)
    k_real = 0.1         # Constante de enfriamiento
    
    # Generar tiempos de medición
    tiempos = np.linspace(0, 30, 30)
    
    # Generar temperaturas con ruido
    temperaturas_teoricas = T_amb_real + (T_ini_real - T_amb_real) * np.exp(-k_real * tiempos)
    ruido = np.random.normal(0, 2, len(tiempos))  # Ruido de medición
    temperaturas = temperaturas_teoricas + ruido
    
    print("Datos experimentales generados:")
    print(f"  - Parámetros reales: T_amb={T_amb_real}, T_ini={T_ini_real}, k={k_real}")
    print(f"  - {len(tiempos)} puntos de medición")
    print(f"  - Ruido gaussiano con σ=2°C")
    
    return tiempos, temperaturas, (T_amb_real, T_ini_real, k_real)


# ============================================================================
# MODELO DE ENFRIAMIENTO
# ============================================================================

def modelo_enfriamiento(t, parametros):
    """
    Modelo de enfriamiento de Newton:
    T(t) = T_amb + (T_ini - T_amb) * exp(-k*t)
    
    Parámetros:
    -----------
    t : array
        Tiempos
    parametros : array [T_amb, T_ini, k]
        Parámetros del modelo
    """
    T_amb, T_ini, k = parametros
    return T_amb + (T_ini - T_amb) * np.exp(-k * t)


# ============================================================================
# FUNCIÓN OBJETIVO: ERROR CUADRÁTICO MEDIO
# ============================================================================

# Variables globales para los datos (necesarias para la función objetivo)
tiempos_globales = None
temperaturas_globales = None

def error_ajuste(parametros):
    """
    Calcula el error cuadrático medio entre el modelo y los datos.
    Esta es la función que DE minimizará.
    
    Parámetros:
    -----------
    parametros : array [T_amb, T_ini, k]
        Parámetros a optimizar
        
    Returns:
    --------
    error : float
        Error cuadrático medio (MSE)
    """
    # Predecir temperaturas con estos parámetros
    T_predichas = modelo_enfriamiento(tiempos_globales, parametros)
    
    # Calcular error cuadrático medio
    mse = np.mean((temperaturas_globales - T_predichas)**2)
    
    # Añadir penalización si k es negativo (no tiene sentido físico)
    if parametros[2] < 0:
        mse += 1000
    
    return mse


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def ajustar_curva_con_DE():
    """
    Usa Evolución Diferencial para encontrar los mejores parámetros
    que ajustan el modelo a los datos experimentales.
    """
    global tiempos_globales, temperaturas_globales
    
    print("="*70)
    print("AJUSTE DE CURVAS CON EVOLUCIÓN DIFERENCIAL")
    print("Problema: Encontrar parámetros de un modelo de enfriamiento")
    print("="*70)
    print()
    
    # 1. Generar datos experimentales
    tiempos_globales, temperaturas_globales, params_reales = generar_datos_experimentales()
    
    print()
    print("-"*70)
    print("Iniciando optimización con Evolución Diferencial...")
    print("-"*70)
    print()
    
    # 2. Definir límites de búsqueda para cada parámetro
    # [T_ambiente, T_inicial, k]
    limites = [
        (0, 50),      # T_ambiente: entre 0 y 50 °C
        (50, 150),    # T_inicial: entre 50 y 150 °C
        (0.01, 1.0)   # k: entre 0.01 y 1.0
    ]
    
    # 3. Crear instancia de Evolución Diferencial
    de = EvolucionDiferencial(
        funcion_objetivo=error_ajuste,
        limites=limites,
        tamaño_poblacion=60,
        F=0.8,
        CR=0.9,
        max_generaciones=150
    )
    
    # 4. Ejecutar optimización
    mejores_parametros, error_final = de.optimizar(verbose=True)
    
    # 5. Extraer parámetros encontrados
    T_amb_encontrado, T_ini_encontrado, k_encontrado = mejores_parametros
    T_amb_real, T_ini_real, k_real = params_reales
    
    # 6. Mostrar resultados
    print()
    print("="*70)
    print("COMPARACIÓN DE RESULTADOS")
    print("="*70)
    print()
    print(f"{'Parámetro':<20} {'Valor Real':<15} {'Valor Encontrado':<15} {'Error %':<10}")
    print("-"*70)
    print(f"{'T_ambiente (°C)':<20} {T_amb_real:<15.2f} {T_amb_encontrado:<15.2f} {abs(T_amb_real-T_amb_encontrado)/T_amb_real*100:<10.2f}%")
    print(f"{'T_inicial (°C)':<20} {T_ini_real:<15.2f} {T_ini_encontrado:<15.2f} {abs(T_ini_real-T_ini_encontrado)/T_ini_real*100:<10.2f}%")
    print(f"{'k (constante)':<20} {k_real:<15.3f} {k_encontrado:<15.3f} {abs(k_real-k_encontrado)/k_real*100:<10.2f}%")
    print("="*70)
    print(f"Error cuadrático medio final: {error_final:.4f}")
    print("="*70)
    
    # 7. Visualizar resultados
    visualizar_resultados(tiempos_globales, temperaturas_globales, 
                         mejores_parametros, params_reales, de)
    
    return de, mejores_parametros


def visualizar_resultados(tiempos, temperaturas, params_encontrados, params_reales, de):
    """
    Crea visualizaciones de los resultados del ajuste.
    """
    fig = plt.figure(figsize=(15, 5))
    
    # Gráfica 1: Datos experimentales vs modelo ajustado
    plt.subplot(1, 3, 1)
    
    # Datos experimentales
    plt.scatter(tiempos, temperaturas, color='red', s=50, alpha=0.6, 
                label='Datos experimentales', zorder=3)
    
    # Modelo con parámetros reales
    t_continuo = np.linspace(0, 30, 300)
    T_real = modelo_enfriamiento(t_continuo, params_reales)
    plt.plot(t_continuo, T_real, 'b--', linewidth=2, 
             label='Modelo real (sin ruido)', alpha=0.7)
    
    # Modelo con parámetros encontrados
    T_ajustado = modelo_enfriamiento(t_continuo, params_encontrados)
    plt.plot(t_continuo, T_ajustado, 'g-', linewidth=2.5, 
             label='Modelo ajustado (DE)', zorder=2)
    
    plt.xlabel('Tiempo (minutos)', fontsize=11)
    plt.ylabel('Temperatura (°C)', fontsize=11)
    plt.title('Ajuste de Curva con Evolución Diferencial', fontsize=12)
    plt.legend(fontsize=9)
    plt.grid(True, alpha=0.3)
    
    # Gráfica 2: Convergencia del algoritmo
    plt.subplot(1, 3, 2)
    plt.plot(de.historial_mejor_fitness, 'b-', linewidth=2)
    plt.xlabel('Generación', fontsize=11)
    plt.ylabel('Error Cuadrático Medio', fontsize=11)
    plt.title('Convergencia del Algoritmo', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.yscale('log')
    
    # Gráfica 3: Residuos (diferencias entre datos y modelo)
    plt.subplot(1, 3, 3)
    T_predichas = modelo_enfriamiento(tiempos, params_encontrados)
    residuos = temperaturas - T_predichas
    
    plt.scatter(tiempos, residuos, color='purple', s=50, alpha=0.6)
    plt.axhline(y=0, color='black', linestyle='--', linewidth=1)
    plt.xlabel('Tiempo (minutos)', fontsize=11)
    plt.ylabel('Residuo (°C)', fontsize=11)
    plt.title('Análisis de Residuos', fontsize=12)
    plt.grid(True, alpha=0.3)
    
    # Calcular estadísticas de residuos
    residuo_medio = np.mean(residuos)
    residuo_std = np.std(residuos)
    plt.text(0.02, 0.98, f'Media: {residuo_medio:.2f}°C\nσ: {residuo_std:.2f}°C',
             transform=plt.gca().transAxes, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.show()


# ============================================================================
# OTRO EJEMPLO: AJUSTAR UNA FUNCIÓN SENO CON RUIDO
# ============================================================================

def ejemplo_ajuste_sinusoidal():
    """
    Ejemplo adicional: Ajustar una función sinusoidal.
    Modelo: y = A * sin(ω*x + φ) + C
    """
    global tiempos_globales, temperaturas_globales
    
    print("\n" + "="*70)
    print("EJEMPLO ADICIONAL: Ajuste de Función Sinusoidal")
    print("="*70)
    
    # Generar datos
    x = np.linspace(0, 10, 50)
    A_real, omega_real, phi_real, C_real = 3.0, 2.0, 0.5, 1.0
    y_real = A_real * np.sin(omega_real * x + phi_real) + C_real
    y_con_ruido = y_real + np.random.normal(0, 0.3, len(x))
    
    tiempos_globales = x
    temperaturas_globales = y_con_ruido
    
    def modelo_seno(x, params):
        A, omega, phi, C = params
        return A * np.sin(omega * x + phi) + C
    
    def error_seno(params):
        y_pred = modelo_seno(tiempos_globales, params)
        return np.mean((temperaturas_globales - y_pred)**2)
    
    # Límites: [A, omega, phi, C]
    limites = [(0, 10), (0, 5), (-np.pi, np.pi), (-5, 5)]
    
    de = EvolucionDiferencial(
        funcion_objetivo=error_seno,
        limites=limites,
        tamaño_poblacion=80,
        F=0.8,
        CR=0.9,
        max_generaciones=200
    )
    
    mejores_params, error = de.optimizar(verbose=True)
    A_enc, omega_enc, phi_enc, C_enc = mejores_params
    
    print()
    print("Parámetros reales vs encontrados:")
    print(f"  A:     {A_real:.3f} vs {A_enc:.3f}")
    print(f"  ω:     {omega_real:.3f} vs {omega_enc:.3f}")
    print(f"  φ:     {phi_real:.3f} vs {phi_enc:.3f}")
    print(f"  C:     {C_real:.3f} vs {C_enc:.3f}")
    
    # Visualizar
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.scatter(x, y_con_ruido, color='red', s=30, alpha=0.6, label='Datos')
    x_cont = np.linspace(0, 10, 200)
    y_ajustado = modelo_seno(x_cont, mejores_params)
    plt.plot(x_cont, y_ajustado, 'g-', linewidth=2, label='Ajuste DE')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Ajuste Sinusoidal')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.subplot(1, 2, 2)
    plt.plot(de.historial_mejor_fitness, linewidth=2)
    plt.xlabel('Generación')
    plt.ylabel('MSE')
    plt.title('Convergencia')
    plt.grid(True, alpha=0.3)
    plt.yscale('log')
    
    plt.tight_layout()
    plt.show()


# ============================================================================
# EJECUCIÓN
# ============================================================================

if __name__ == "__main__":
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "APLICACIÓN PRÁCTICA: AJUSTE DE CURVAS" + " "*16 + "║")
    print("║" + " "*10 + "Usando Algoritmo de Evolución Diferencial" + " "*17 + "║")
    print("╚" + "="*68 + "╝")
    print()
    
    # Ejemplo 1: Ajuste de curva de enfriamiento
    de, params = ajustar_curva_con_DE()
    
    # Ejemplo 2: Ajuste de función sinusoidal (descomenta para ejecutar)
    # ejemplo_ajuste_sinusoidal()
    
    print("\n" + "="*70)
    print("¡Ejemplos completados exitosamente!")
    print("="*70)
    print()
    print("💡 NOTA: Este tipo de ajuste de curvas es muy útil en:")
    print("   - Análisis de datos experimentales")
    print("   - Modelado físico y químico")
    print("   - Calibración de sensores")
    print("   - Predicción de tendencias")
    print("   - Machine Learning (regresión no lineal)")

