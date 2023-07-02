# Bot de Enigmas y Acertijos Matemáticos para Telegram

Este bot de Telegram está diseñado para proporcionar enigmas y acertijos matemáticos a los usuarios de telegram.
Puedes probar el bot en vivo [aquí](https://t.me/enigmatica_acertijos_bot).

## Instrucciones de Instalación

Sigue estos pasos para instalar y configurar el bot:

### 1. Crear un entorno virtual con venv

```bash
python3 -m venv venv
```

### 2. Activar el entorno virtual

En Windows:

```bash
.\venv\Scripts\activate
```

En Unix o MacOS:

```bash
source venv/bin/activate
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 4. Copiar el archivo de configuración

```bash
cp config.default.py config.py
```

### 5. Crear un bot en Telegram

Para crear un bot en Telegram, necesitarás hablar con BotFather. Puedes hacer esto siguiendo estos pasos:

- Busca 'BotFather' en la barra de búsqueda de Telegram y haz clic en el bot correspondiente.
- Haz clic en el botón 'Start' o escribe `/start`.
- Para crear un nuevo bot, escribe `/newbot` y sigue las instrucciones. BotFather te proporcionará un token para tu nuevo bot.

### 6. Reemplazar el token de Telegram en el archivo de configuración

Reemplaza la variable `telegram_token` en `config.py` con el token que BotFather te proporcionó en el paso anterior.

### 7. Ejecutar el bot

```bash
python main.py
```

Ahora, tu bot de Telegram debería estar funcionando. Puedes buscar el nombre de tu bot en Telegram y comenzar a usarlo.

---

Este archivo README proporciona una guía paso a paso para instalar y configurar tu bot de enigmas matemáticos. Espero que te resulte útil.

## Agradecimientos
Me gustaria agradecer mucho a mi abuela Erika que me siempre buscó incentivarme con éste tipo de enigmas y ejercicios para la mente desde que yo era chico. 

Luego, la mayoría de los ejercicios de éste juego fueron extraídos del libro ENIGMÁTICA del autor Lluís Segarra. Mis agradecimientos a él y a su equipo.


