# Установка FFmpeg (Linux, macOS, Windows)

`ffmpeg` — это утилита командной строки для работы с видео и аудио. Используется для конвертации, обработки и анализа медиафайлов.

---

## Установка на Linux

### Debian/Ubuntu:

```bash
sudo apt update
sudo apt install ffmpeg
```

### Arch Linux / Manjaro:

```bash
sudo pacman -S ffmpeg
```

### Fedora:

```bash
sudo dnf install ffmpeg ffmpeg-devel
```

### Проверка установки:

```bash
ffmpeg -version
```

---

## Установка на macOS

### Через Homebrew:

1. Установи Homebrew, если он не установлен:
   [https://brew.sh](https://brew.sh)

2. Установи `ffmpeg`:

```bash
brew install ffmpeg
```

### Проверка:

```bash
ffmpeg -version
```

---

## Установка на Windows

1. Перейди на официальный сайт: [https://www.gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/)

2. Скачай архив **"ffmpeg-release-essentials.zip"**

3. Распакуй архив, например, в `C:\ffmpeg`

4. Добавь в системный `PATH`:

   - Открой «Переменные среды»
   - Найди `Path` -> нажми «Изменить» -> «Создать» -> добавь:

     ```
     C:\ffmpeg\bin
     ```

5. Перезапусти терминал/командную строку.

6. Проверка:

```cmd
ffmpeg -version
```
