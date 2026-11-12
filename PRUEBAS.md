# Comprobaciones visibles de M2

Comprueba cada método antes de continuar con el siguiente:

- nivel válido y nivel inexistente; 
```Se comprueba que el programa responde correctamente cuando la ruta del nivel no existe, no corresponde a un archivo o contiene un nivel no válido```
- nivel con filas de distinta longitud;
```Se verifica que el juego funciona adecuadamente aunque las filas tengan diferentes cantidades de bloques```
- paleta en ambos límites de la pantalla;
```Se garantiza que la paleta permanece dentro de los límites de la pantalla incluso al continuar desplazándola```
- rebote contra pared, paleta y cada tipo de bloque;
```Se comprueba que la pelota rebota correctamente al entrar en contacto con las paredes, la paleta y los distintos bloques, aplicando la puntuación correspondiente en cada caso```
- pérdida de una vida y reinicio de la bola;
```Se verifica que se descuenta una vida cuando la pelota cae y que, tras perderla, vuelve a colocarse correctamente sobre la paleta```
- victoria al eliminar el último bloque y derrota al agotar vidas;
```Se comprueba que aparece el aviso de victoria al destruir todos los bloques y el de derrota cuando se pierden todas las vidas```
- salida limpia con Escape y al cerrar la ventana.
```Se garantiza que el juego se cierra correctamente, tanto al pulsar la tecla Escape como al cerrar la ventana, sin provocar errores```

Una mejora opcional no debe romper ninguno de estos casos.
