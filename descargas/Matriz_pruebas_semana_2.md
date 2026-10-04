# Matriz de pruebas del Alpha 0.5 Estable

La columna de resultado obtenido debe completarse después de ejecutar el ZIP en el equipo de entrega. No se deben registrar como aprobadas pruebas que todavía no fueron observadas.

| ID | Elemento | Resultado esperado | Resultado obtenido | Estado |
|---|---|---|---|---|
| P01 | Controles | Juan responde a WASD y flechas en cuatro direcciones. | Pendiente de ejecución local. | Pendiente |
| P02 | Colisiones | Juan no atraviesa casas, rocas ni límites. | Pendiente de ejecución local. | Pendiente |
| P03 | Cámara | La cámara sigue a Juan sin salir del mapa. | Pendiente de ejecución local. | Pendiente |
| P04 | Objetivo | El HUD muestra una acción comprensible. | Pendiente de ejecución local. | Pendiente |
| P05 | NPC | Florencio inicia diálogo solamente dentro del área. | Pendiente de ejecución local. | Pendiente |
| P06 | Estados NPC | El diálogo cambia después de obtener la pista. | Pendiente de ejecución local. | Pendiente |
| P07 | Pista | La pista se recoge una sola vez y actualiza el HUD. | Pendiente de ejecución local. | Pendiente |
| P08 | Enemigo | La sombra patrulla, detecta, persigue y produce daño. | Pendiente de ejecución local. | Pendiente |
| P09 | Combate | Dos ataques dirigidos dispersan la sombra. | Pendiente de ejecución local. | Pendiente |
| P10 | Reinicio | Perder tres puntos de salud devuelve a Juan al checkpoint. | Pendiente de ejecución local. | Pendiente |
| P11 | Core loop | Hablar, explorar, superar riesgo, recoger pista y salir forma un recorrido completo. | Pendiente de ejecución local. | Pendiente |
| P12 | API | El servidor guarda y recupera nivel, pista y checkpoint. | Cubierto por pruebas automáticas; confirmar en demostración. | Verificar |
| P13 | Validación | El servidor rechaza checkpoint y progresión inválidos. | Cubierto por pruebas automáticas; confirmar resultado de pytest. | Verificar |
| P14 | Desconexión | Si FastAPI está apagado, el cliente no se cierra y muestra el estado. | Pendiente de ejecución local. | Pendiente |
| P15 | Nueva partida | `N` o `n` crea otra sesión y empieza directamente sin un segundo Enter. | Pendiente de ejecución local. | Pendiente |
| P16 | Pausa real | Con `Esc`, Juan y las cinco sombras quedan inmóviles hasta reanudar. | Pendiente de ejecución local. | Pendiente |
| P17 | Persistencia exacta | Tras guardar con `G`, salir con `F8` y reabrir, se recuperan misión, salud y posición. | Cubierto en API; confirmar la integración en Godot. | Verificar |
| P18 | Migración SQLite | Una base de datos anterior recibe los nuevos campos sin perder registros. | Cubierto por prueba automática de servidor. | Verificar |
