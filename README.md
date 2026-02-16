# Taller de Compiladores - Análisis Léxico

## Autor
Juan Camilo Echavarría Sepúlveda

## Descripción
Implementación de un analizador léxico básico que reconoce tokens según las especificaciones del taller.

## Lenguaje soportado
- **Palabras reservadas**: `if`, `else`, `while`
- **Identificadores**: Letras mayúsculas/minúsculas seguidas de letras o números
- **Números enteros**: Dígitos del 0-9
- **Operadores**: `+`, `-`, `*`, `/`, `=`
- **Delimitadores**: `(`, `)`, `;`

## Requisitos
- Python 3.7 o superior
- Módulo `re` (incluido en Python estándar)
- Módulo `typing` (incluido en Python estándar)

## Instalación y Ejecución

### 1. Descargar los archivos
```bash
# Copiar lexer.py a tu directorio de trabajo
```

### 2. Ejecutar el programa
```bash
python lexer.py
```

### 3. Modo interactivo (opcional)
Descomentar la última línea del archivo `lexer.py`:
```python
# ejecutar_interactivo()  # Descomentar esta línea
```

## Ejemplos de Uso

### Código de ejemplo del taller
```
if (x = 10) x = x + 1;
```

### Salida esperada
```
==================================================
ANÁLISIS LÉXICO
==================================================
Código de entrada: if (x = 10) x = x + 1;

Tokens generados:
------------------------------
 1. Token(PALABRA_RESERVADA, 'if', línea:1, col:1)
 2. Token(DELIMITADOR, '(', línea:1, col:4)
 3. Token(IDENTIFICADOR, 'x', línea:1, col:5)
 4. Token(OPERADOR, '=', línea:1, col:7)
 5. Token(ENTERO, '10', línea:1, col:9)
 6. Token(DELIMITADOR, ')', línea:1, col:11)
 7. Token(IDENTIFICADOR, 'x', línea:1, col:13)
 8. Token(OPERADOR, '=', línea:1, col:15)
 9. Token(IDENTIFICADOR, 'x', línea:1, col:17)
10. Token(OPERADOR, '+', línea:1, col:19)
11. Token(ENTERO, '1', línea:1, col:21)
12. Token(DELIMITADOR, ';', línea:1, col:22)

Total de tokens: 12
```

## Características Implementadas

### ✅ Parte A - Identificación de lexemas
- Reconoce correctamente todos los lexemas del código de ejemplo

### ✅ Parte B - Patrones
- **Identificador**: `\b[a-zA-Z][a-zA-Z0-9]*\b`
- **Entero**: `\b[0-9]+\b`
- **Operador**: `[+\-*/=]`
- **Delimitador**: `[();]`

### ✅ Parte C - Reflexión
- Las palabras reservadas se evalúan primero para distinguirlas de identificadores
- El orden de las reglas es crucial para la correcta clasificación

### ✅ Parte D - Codificación
- Implementación completa en Python
- Manejo de errores léxicos
- Información de posición (línea, columna)
- Estadísticas de análisis
- Modo interactivo opcional

## Estructura del Código

### Clases principales
- **`Token`**: Representa un token con tipo, valor y posición
- **`TokenType`**: Constantes para tipos de tokens
- **`LexerError`**: Excepción para errores léxicos
- **`Lexer`**: Analizador léxico principal

### Métodos importantes
- `tokenizar()`: Convierte texto en lista de tokens
- `analizar_codigo()`: Analiza y muestra resultados formateados
- `obtener_estadisticas()`: Genera estadísticas de tokens

## Pruebas Realizadas

### Casos de prueba exitosos
1. `if (x = 10) x = x + 1;` → 12 tokens
2. `while (i = 0) i = i + 1;` → 12 tokens
3. `if (a = b) a = a * 2;` → 11 tokens
4. `x = 5; y = x + 10;` → 10 tokens
5. `if (resultado = 100) resultado = resultado / 2;` → 13 tokens

### Detección de errores
- Caracteres no válidos (ej: `@`, `#`, `$`)
- Mensajes de error con posición exacta

## Buenas Prácticas Aplicadas
- Documentación completa con docstrings
- Type hints para mejor legibilidad
- Encapsulación con métodos privados
- Manejo de excepciones específico
- Código modular y reutilizable
- Constantes definidas en clases

## Notas del Desarrollador
Este analizador léxico implementa correctamente los conceptos fundamentales del análisis léxico, demostrando la importancia del orden de las reglas y el manejo de errores en compiladores.
