"""
Módulo: Analizador Léxico Básico
Autor: Juan Camilo Echavarría Sepúlveda
Descripción: Implementación de un analizador léxico para el taller de compiladores
Versión: 1.0

Este módulo implementa un analizador léxico básico que reconoce:
- Palabras reservadas: if, else, while
- Identificadores: letras mayúsculas y minúsculas seguidas de letras o números
- Números enteros
- Operadores: +, -, *, /, =
- Delimitadores: (, ), ;
"""

import re
from typing import List, Tuple, Optional


class TokenType:
    """Constantes para los tipos de tokens."""
    PALABRA_RESERVADA = "PALABRA_RESERVADA"
    IDENTIFICADOR = "IDENTIFICADOR"
    ENTERO = "ENTERO"
    OPERADOR = "OPERADOR"
    DELIMITADOR = "DELIMITADOR"


class Token:
    """Representa un token con su tipo y valor."""
    
    def __init__(self, tipo: str, valor: str, linea: int = 1, columna: int = 0):
        self.tipo = tipo
        self.valor = valor
        self.linea = linea
        self.columna = columna
    
    def __repr__(self) -> str:
        return f"Token({self.tipo}, '{self.valor}', línea:{self.linea}, col:{self.columna})"


class LexerError(Exception):
    """Excepción para errores léxicos."""
    
    def __init__(self, mensaje: str, linea: int = 1, columna: int = 0):
        self.mensaje = mensaje
        self.linea = linea
        self.columna = columna
        super().__init__(f"Error léxico en línea {linea}, columna {columna}: {mensaje}")


class Lexer:
    """Analizador léxico básico."""
    
    def __init__(self):
        """Inicializa el lexer con patrones y palabras reservadas."""
        self._palabras_reservadas = {
            'if': TokenType.PALABRA_RESERVADA,
            'else': TokenType.PALABRA_RESERVADA,
            'while': TokenType.PALABRA_RESERVADA
        }
        
        self._patrones = self._inicializar_patrones()
        self._linea_actual = 1
        self._columna_actual = 0
    
    def _inicializar_patrones(self) -> List[Tuple[re.Pattern, str]]:
        """Inicializa los patrones de expresiones regulares."""
        patrones = [
            # Palabras reservadas (van primero)
            (r'\b(if|else|while)\b', TokenType.PALABRA_RESERVADA),
            # Identificadores: empiezan con letra, seguido de letras o números
            (r'\b[a-zA-Z][a-zA-Z0-9]*\b', TokenType.IDENTIFICADOR),
            # Números enteros
            (r'\b[0-9]+\b', TokenType.ENTERO),
            # Operadores
            (r'[+\-*/=]', TokenType.OPERADOR),
            # Delimitadores
            (r'[();]', TokenType.DELIMITADOR),
            # Espacios en blanco (ignorar)
            (r'\s+', None)
        ]
        
        compilados = []
        for patron, tipo in patrones:
            compilados.append((re.compile(patron), tipo))
        
        return compilados
    
    def _actualizar_posicion(self, texto: str, posicion: int):
        """Actualiza la línea y columna actual basado en la posición."""
        # Contar saltos de línea hasta la posición actual
        lineas_hasta_posicion = texto[:posicion].count('\n')
        if lineas_hasta_posicion > 0:
            self._linea_actual += lineas_hasta_posicion
            # Encontrar la última línea
            ultima_linea_inicio = texto.rfind('\n', 0, posicion)
            self._columna_actual = posicion - ultima_linea_inicio
        else:
            self._columna_actual = posicion + 1
    
    def tokenizar(self, texto: str) -> List[Token]:
        """
        Convierte el texto de entrada en una lista de tokens.
        
        Args:
            texto: Código fuente a analizar
            
        Returns:
            Lista de tokens encontrados
            
        Raises:
            LexerError: Si encuentra un carácter no reconocido
        """
        tokens = []
        posicion = 0
        longitud = len(texto)
        self._linea_actual = 1
        self._columna_actual = 0
        
        while posicion < longitud:
            self._actualizar_posicion(texto, posicion)
            
            match_encontrado = False
            
            # Intentar hacer match con cada patrón en orden
            for patron, tipo in self._patrones:
                match = patron.match(texto, posicion)
                if match:
                    lexema = match.group(0)
                    
                    # Si es espacio en blanco, solo avanzar la posición
                    if tipo is None:
                        posicion = match.end()
                        match_encontrado = True
                        break
                    
                    # Crear token con información de posición
                    token = Token(
                        tipo=tipo,
                        valor=lexema,
                        linea=self._linea_actual,
                        columna=self._columna_actual
                    )
                    
                    # Verificar si es palabra reservada vs identificador
                    if token.tipo == TokenType.IDENTIFICADOR:
                        if lexema in self._palabras_reservadas:
                            token.tipo = TokenType.PALABRA_RESERVADA
                    
                    tokens.append(token)
                    posicion = match.end()
                    match_encontrado = True
                    break
            
            # Si no se encontró ningún match, hay un error léxico
            if not match_encontrado:
                if posicion < longitud:
                    caracter = texto[posicion]
                    raise LexerError(
                        f"Carácter no reconocido: '{caracter}'",
                        self._linea_actual,
                        self._columna_actual
                    )
                else:
                    break
        
        return tokens
    
    def analizar_codigo(self, codigo: str) -> List[Token]:
        """
        Analiza código y muestra resultados formateados.
        
        Args:
            codigo: Código fuente a analizar
            
        Returns:
            Lista de tokens generados
        """
        print("=" * 50)
        print("ANÁLISIS LÉXICO")
        print("=" * 50)
        print(f"Código de entrada: {codigo}")
        print()
        
        try:
            tokens = self.tokenizar(codigo)
            
            print("Tokens generados:")
            print("-" * 30)
            for i, token in enumerate(tokens, 1):
                print(f"{i:2d}. {token}")
            
            print(f"\nTotal de tokens: {len(tokens)}")
            return tokens
            
        except LexerError as e:
            print(f"\nError: {e}")
            return []
    
    def obtener_estadisticas(self, tokens: List[Token]) -> dict:
        """
        Genera estadísticas sobre los tokens analizados.
        
        Args:
            tokens: Lista de tokens analizados
            
        Returns:
            Diccionario con estadísticas
        """
        estadisticas = {}
        for token in tokens:
            estadisticas[token.tipo] = estadisticas.get(token.tipo, 0) + 1
        return estadisticas


def main():
    """Función principal para demostrar el analizador léxico."""
    # Crear instancia del lexer
    lexer = Lexer()
    
    # Código de ejemplo del taller
    codigo_ejemplo = "if (x = 10) x = x + 1;"
    
    # Analizar el código principal
    tokens = lexer.analizar_codigo(codigo_ejemplo)
    
    if tokens:
        # Mostrar estadísticas
        estadisticas = lexer.obtener_estadisticas(tokens)
        print("\nEstadísticas de tokens:")
        print("-" * 25)
        for tipo, cantidad in estadisticas.items():
            print(f"{tipo}: {cantidad}")
    
    # Pruebas adicionales
    print("\n" + "=" * 50)
    print("PRUEBAS ADICIONALES")
    print("=" * 50)
    
    codigos_prueba = [
        "while (i = 0) i = i + 1;",
        "if (a = b) a = a * 2;",
        "x = 5; y = x + 10;",
        "if (resultado = 100) resultado = resultado / 2;"
    ]
    
    for i, codigo in enumerate(codigos_prueba, 1):
        print(f"\nPrueba {i}: {codigo}")
        try:
            tokens_prueba = lexer.tokenizar(codigo)
            for token in tokens_prueba:
                print(f"  {token}")
        except LexerError as e:
            print(f"  Error: {e}")
    
    # Prueba con error léxico
    print("\n" + "=" * 50)
    print("PRUEBA CON ERROR LÉXICO")
    print("=" * 50)
    codigo_con_error = "if (x = @10) x = x + 1;"
    print(f"Código con error: {codigo_con_error}")
    try:
        lexer.analizar_codigo(codigo_con_error)
    except LexerError as e:
        print(f"Error detectado correctamente: {e}")


def ejecutar_interactivo():
    """Modo interactivo para analizar código ingresado por el usuario."""
    lexer = Lexer()
    
    print("\n" + "=" * 50)
    print("MODO INTERACTIVO - ANALIZADOR LÉXICO")
    print("=" * 50)
    print("Ingrese 'salir' para terminar")
    
    while True:
        try:
            codigo = input("\nIngrese el código a analizar: ").strip()
            
            if codigo.lower() == 'salir':
                print("Hasta pronto!")
                break
            
            if not codigo:
                print("Por favor ingrese un código válido.")
                continue
            
            lexer.analizar_codigo(codigo)
            
        except KeyboardInterrupt:
            print("\n\nPrograma interrumpido. Hasta pronto!")
            break
        except Exception as e:
            print(f"\nError inesperado: {e}")


if __name__ == "__main__":
    main()
    
    # Descomentar la siguiente línea para activar el modo interactivo
    # ejecutar_interactivo()
