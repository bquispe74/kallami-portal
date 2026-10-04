# Defensa final de Kallami: Senderos de Plata

## Apertura de 30 segundos

“Kallami: Senderos de Plata es una aventura narrativa 2D construida en Godot. La versión final transforma el prototipo inicial en tres niveles conectados: comunidad, ascenso y cámara de plata. Integra memorias, combate a distancia, exploración con niebla, diálogo con voz sintetizada, rompecabezas final y perfiles que conservan su propio avance en un servidor FastAPI. La historia no presenta la plata solo como premio; la contrapone con la memoria de la comunidad y el relato del cerro.”

## Orden recomendado de la exposición

### 1. Problema y propuesta

Explica que el prototipo debía reunir narrativa, exploración y una integración cliente-servidor verificable. La solución usa un pueblo inspirado visualmente en el altiplano, un sendero largo y objetivos breves que siempre aparecen en el HUD.

### 2. Ciclo jugable

Muestra este flujo sin abrir el editor:

```text
Hablar con Florencio
        ↓
Cruzar la comunidad
        ↓
Ascender y combatir sombras
        ↓
Recoger tres memorias
        ↓
Entrar a la cámara de plata
        ↓
Vencer guardianes y ordenar los hechos
        ↓
Activar el altar final
```

La barra sobre Juan comunica daño sin obligar a mirar una esquina. Verde representa un estado seguro, amarillo advierte y rojo indica peligro inmediato. El minimapa no entrega la solución: registra lo recorrido.

### 3. Arquitectura técnica

```text
[Godot 4.7.2]
  UI + gameplay + audio
          |
          | HTTP / JSON + Bearer token
          v
[FastAPI 1.1]
  perfiles + validación
          |
          v
[SQLite]
  hash PIN + progreso independiente
```

El cliente se ocupa de la experiencia de juego. El servidor decide si una transición es válida: comprueba checkpoints, memorias únicas, avance monotónico, límites del mapa y pertenencia del token.

### 4. Evidencia de persistencia

1. Juega hasta recoger una memoria o perder vida.
2. Pulsa `G`.
3. Señala en el HUD `Progreso guardado` y en la terminal `POST /api/progreso ... 200 OK`.
4. Cierra la ejecución con `F8`.
5. Vuelve a ejecutar, elige el mismo perfil e ingresa su PIN.
6. Señala `GET /api/progreso/<perfil> ... 200 OK`.
7. Comprueba visualmente que reaparecen el nivel, posición, vida, memorias, misión, checkpoint y paso del rompecabezas.

> Nota: el `200 OK` prueba que el servidor aceptó la operación. La restauración visual posterior demuestra que los datos no solo llegaron, sino que se consultaron y aplicaron correctamente.

### 5. Seguridad aplicada

El sistema no guarda el PIN. Deriva una clave con **PBKDF2-HMAC-SHA256**, sal aleatoria y 210 000 iteraciones. Un login correcto rota un token de 256 bits; las rutas de progreso exigen `Authorization: Bearer ...`. Las consultas SQLite usan parámetros, y la lógica rechaza pistas duplicadas, saltos de progreso y tokens cruzados entre perfiles.

Para mostrar evidencia reproducible, ejecuta:

```bash
brayanux@debian:~/Workspace/inf_266/Kallami_Final_v1.0/servidor$ ./probar_servidor.sh
............                                                             [100%]
12 passed
```

No presentes el PIN de cuatro dígitos como autenticación de producción. Es una medida proporcional a una aplicación local académica. Una versión publicada necesitaría HTTPS, límite de intentos, expiración de sesiones y recuperación de cuenta.

## Mejoras visibles frente al Alpha

- El mapa creció de 1600×900 a 2400×1500 y ahora tiene pueblo, plaza, cultivos, terrazas y ruta al cerro.
- La cámara acerca los elementos; Juan y Florencio se leen mejor en pantalla.
- El ataque produce una onda de honda y una piedra física con alcance e impacto.
- Hay tres sombras en la comunidad, nueve durante el ascenso y dos guardianes finales.
- La vida aparece sobre el protagonista y cambia de color.
- La niebla limita la vista; las huellas de luz y el minimapa registran la exploración.
- Florencio usa un retrato de medio cuerpo, boca animada, texto progresivo y cinco clips de voz sintetizada localmente.
- Cada nivel tiene un ambiente propio y la tensión aumenta según la distancia del enemigo.
- Tres memorias abren la cámara, donde un rompecabezas narrativo habilita el altar final.
- El servidor conserva el nivel y el avance parcial del rompecabezas, además de vida, posición y pistas.
- Los perfiles permiten crear, entrar, eliminar y separar partidas.

## Preguntas probables y respuestas breves

### ¿Por qué el minimapa no muestra todo?

Porque forma parte de la mecánica. Reduce la desorientación, pero mantiene la exploración: solo pinta celdas visitadas y objetivos ya descubiertos.

### ¿El mapa representa exactamente el Cerro Kallami?

No. Es una interpretación ficticia para el prototipo. Usa referencias visuales del altiplano, pero no afirma reconstruir un sitio histórico ni un relato oral literal.

### ¿Cómo cambia la música?

Un director de audio calcula la distancia al enemigo válido más cercano. Al reducirse esa distancia, baja el ambiente y sube de forma gradual la capa de tensión. Cuando la amenaza se aleja, la mezcla vuelve al pueblo.

### ¿Qué sucede si alguien altera el JSON?

El servidor no confía en el contador del cliente. Compara la lista de identificadores únicos, verifica el orden de avance, los checkpoints y la sesión del perfil. Una transición imposible responde `409` o `422`.

### ¿Por qué FastAPI y SQLite?

FastAPI permite un contrato claro, documentación automática y validación de modelos. SQLite basta para una demostración local, conserva los perfiles entre ejecuciones y no requiere instalar un motor de base de datos aparte.

### ¿Qué quedó fuera?

No hay multijugador, servicio remoto, recuperación de PIN ni doblaje humano de estudio. Florencio utiliza una voz sintética local y el movimiento de boca acompaña tanto la reproducción como la aparición del texto. Esta decisión mantiene el alcance defendible y deja claro qué se implementó realmente.

## Cierre de 20 segundos

“La versión final ya demuestra un juego completo y no una colección de pantallas: existen tres niveles, un objetivo, riesgo, exploración, progresión, rompecabezas, cierre y recuperación del estado. La integración con perfiles añade una evidencia concreta de seguridad y persistencia. El tráiler muestra estas mecánicas con captura directa del juego y la suite automatizada respalda el comportamiento del servidor.”
