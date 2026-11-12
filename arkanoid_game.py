"""Plantilla del juego Arkanoid para el hito M2.

Completa los métodos marcados con TODO respetando las anotaciones de tipo y la
estructura de la clase. El objetivo es construir un prototipo jugable usando
pygame que cargue bloques desde un fichero de nivel basado en caracteres.
"""

from arkanoid_core import *

# --------------------------------------------------------------------- #
# Métodos a completar por el alumnado
# --------------------------------------------------------------------- #


@arkanoid_method
def cargar_nivel(self) -> list[str]:
    """Lee el fichero de nivel y devuelve la cuadrícula como lista de filas."""
    # - Comprueba que `self.level_path` existe y es fichero.
    if not self.level_path.exists() or not self.level_path.is_file():
        raise FileNotFoundError(f"No se encuentra el fichero de nivel: {self.level_path}")

    # - Lee su contenido, filtra líneas vacías y valida que todas tienen el mismo ancho.
    lineas = [
        linea
        for linea in self.level_path.read_text(encoding="utf-8").splitlines()
        if linea.strip()
    ]

    if not lineas:
        raise ValueError("El nivel está vacío.")

    ancho_referencia = len(lineas[0])

    for linea in lineas:
        if len(linea) != ancho_referencia:
            raise ValueError("Todas las filas del nivel deben tener la misma longitud.")

    # - Guarda el resultado en `self.layout` y devuélvelo.
    self.layout = lineas
    return self.layout

@arkanoid_method
def preparar_entidades(self) -> None:
    """Posiciona paleta y bola, y reinicia puntuación y vidas."""
    # - Ajusta el tamaño de `self.paddle` y céntrala usando `midbottom`.
    self.paddle.midbottom = (
        self.SCREEN_WIDTH // 2,
        self.SCREEN_HEIGHT - self.PADDLE_OFFSET
    )

    # - Reinicia `self.score`, `self.lives` y `self.end_message`.
    self.score = 0
    self.lives = 3
    self.end_message = ""

    # - Llama a `self.reiniciar_bola()` para colocar la bola sobre la paleta.
    self.reiniciar_bola()


@arkanoid_method
def crear_bloques(self) -> None:
    """Genera los rectángulos de los bloques en base a la cuadrícula."""
    self.blocks.clear()
    self.block_colors.clear()
    self.block_symbols.clear()

    for fila, contenido in enumerate(self.layout):
        for columna, simbolo in enumerate(contenido):
            if simbolo in self.BLOCK_COLORS:
                self.blocks.append(self.calcular_posicion_bloque(fila, columna))
                self.block_colors.append(self.BLOCK_COLORS[simbolo])
                self.block_symbols.append(simbolo)


@arkanoid_method
def procesar_input(self) -> None:
    """Gestiona la entrada de teclado para mover la paleta."""
    teclas = self.obtener_estado_teclas()

    if teclas[self.KEY_LEFT] or teclas[self.KEY_A]:
        self.paddle.x -= int(self.PADDLE_SPEED)
    if teclas[self.KEY_RIGHT] or teclas[self.KEY_D]:
        self.paddle.x += int(self.PADDLE_SPEED)

    if self.paddle.left < 0:
        self.paddle.left = 0
    if self.paddle.right > self.SCREEN_WIDTH:
        self.paddle.right = self.SCREEN_WIDTH


@arkanoid_method
def actualizar_bola(self) -> None:
    """Actualiza la posición de la bola y resuelve colisiones."""

    
    self.ball_pos.x += self.ball_velocity.x
    ball_rect = self.obtener_rect_bola()

    if ball_rect.left <= 0:
        self.ball_pos.x = self.BALL_RADIUS
        self.ball_velocity.x = abs(self.ball_velocity.x)
    elif ball_rect.right >= self.SCREEN_WIDTH:
        self.ball_pos.x = self.SCREEN_WIDTH - self.BALL_RADIUS
        self.ball_velocity.x = -abs(self.ball_velocity.x)

    
    self.ball_pos.y += self.ball_velocity.y
    ball_rect = self.obtener_rect_bola()

    if ball_rect.top <= 0:
        self.ball_pos.y = self.BALL_RADIUS
        self.ball_velocity.y = abs(self.ball_velocity.y)

    
    ball_rect = self.obtener_rect_bola()
    if self.ball_velocity.y > 0 and ball_rect.colliderect(self.paddle):
        self.ball_pos.y = self.paddle.top - self.BALL_RADIUS
        self.ball_velocity.y = -abs(self.ball_velocity.y)

        
        diferencia = (self.ball_pos.x - self.paddle.centerx) / (self.paddle.width / 2)
        self.ball_velocity.x = diferencia * self.BALL_SPEED * 0.8
        if self.ball_velocity.length_squared() > 0:
            self.ball_velocity.scale_to_length(self.BALL_SPEED)

    
    ball_rect = self.obtener_rect_bola()
    for indice, bloque in enumerate(self.blocks):
        if ball_rect.colliderect(bloque):
            simbolo = self.block_symbols[indice]
            self.score += self.BLOCK_POINTS[simbolo]
            self.blocks.pop(indice)
            self.block_colors.pop(indice)
            self.block_symbols.pop(indice)
            self.ball_velocity.y *= -1
            break

    
    if self.ball_pos.y - self.BALL_RADIUS > self.SCREEN_HEIGHT:
        self.lives -= 1
        if self.lives <= 0:
            self.end_message = "¡Has perdido!"
        else:
            self.reiniciar_bola()

    if not self.blocks and not self.end_message:
        self.end_message = "¡Nivel completado!"


@arkanoid_method
def dibujar_escena(self) -> None:
    """Renderiza fondo, bloques, paleta, bola y HUD."""
    # - Rellena el fondo y dibuja cada bloque con `self.dibujar_rectangulo`.
    if self.screen is None:
        return

    self.screen.fill(self.BACKGROUND_COLOR)

    for bloque, color in zip(self.blocks, self.block_colors):
        self.dibujar_rectangulo(bloque, color)

    self.dibujar_rectangulo(self.paddle, self.PADDLE_COLOR)
    self.dibujar_circulo(
        (int(self.ball_pos.x), int(self.ball_pos.y)),
        self.BALL_RADIUS,
        self.BALL_COLOR,
    )

    self.dibujar_texto(f"Puntuación: {self.score}", (20, 20))
    self.dibujar_texto(f"Vidas: {self.lives}", (self.SCREEN_WIDTH - 120, 20))

    if self.end_message:
        ancho_aprox = len(self.end_message) * 15
        posicion = ((self.SCREEN_WIDTH - ancho_aprox) // 2, self.SCREEN_HEIGHT // 2)
        self.dibujar_texto(self.end_message, posicion, grande=True)


@arkanoid_method
def run(self) -> None:
    """Ejecuta el bucle principal del juego."""

    # Inicializa los recursos de Pygame.
    try:
        self.inicializar_pygame()
        self.cargar_nivel()
        self.preparar_entidades()
        self.crear_bloques()

        self.running = True
        while self.running:
            for evento in self.iterar_eventos():
                if evento.type == self.EVENT_QUIT:
                    self.running = False
                elif evento.type == self.EVENT_KEYDOWN and evento.key == self.KEY_ESCAPE:
                    self.running = False

            if not self.running:
                break

            if not self.end_message:
                self.procesar_input()
                self.actualizar_bola()

            self.dibujar_escena()
            self.actualizar_pantalla()

            if self.end_message:
                self.esperar(1800)
                self.running = False

            if self.clock is not None:
                self.clock.tick(self.FPS)
    finally:
        self.finalizar_pygame()


def main() -> None:
    """Permite ejecutar el juego desde la línea de comandos."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Plantilla del hito M2: Arkanoid",
    )
    parser.add_argument(
        "level",
        type=str,
    
        help="Ruta al fichero de nivel (texto con # para bloques y . para huecos).",
    )
    args = parser.parse_args()

    game = ArkanoidGame(args.level)
    game.run()


if __name__ == "__main__":
    main()
