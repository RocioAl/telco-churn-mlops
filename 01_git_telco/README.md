# Práctica 1 — Git: control de versiones

**Objetivo:** aprender a crear un repositorio local, registrar cambios, consultar historial, usar ramas y resolver un conflicto sencillo.

## Requisitos
- Git instalado: https://git-scm.com/downloads
- Visual Studio Code (opcional).
- Windows CMD o terminal de VS Code.

Verifica la instalación:
```bat
git --version
```

## 1. Configurar Git (solo la primera vez en tu computadora)
Reemplaza los valores por tus datos:
```bat
git config --global user.name "Tu Nombre"
git config --global user.email "tu-correo@example.com"
git config --global --list
```

## 2. Crear el repositorio
Abre CMD dentro de esta carpeta:
```bat
git init -b main
git status
git add README.md
git commit -m "Primer commit: agregar README"
git log --oneline
```

## 3. Registrar cambios
Abre `src/clientes.csv` y agrega un cliente ficticio. Después:
```bat
git status
git diff
git add src/clientes.csv
git commit -m "Agregar cliente de ejemplo"
git log --oneline
```

## 4. Ignorar archivos
Crea un archivo local llamado `notas_privadas.txt` y escribe cualquier texto de prueba. Comprueba que `.gitignore` lo excluye:
```bat
git status
```
No debe aparecer como archivo pendiente.

## 5. Crear una rama
```bat
git switch -c mejora-documentacion
```
Edita `README.md`, agrega una sección llamada “Cambios de la rama” y registra el cambio:
```bat
git add README.md
git commit -m "Documentar mejora en rama"
git log --oneline --all --graph
```

## 6. Integrar la rama
```bat
git switch main
git merge mejora-documentacion
git log --oneline --all --graph
```

## 7. Publicar en GitHub (opcional para esta práctica)
Crea en GitHub un repositorio vacío llamado `practica-git-telco` (sin README ni licencia). Sustituye `TU_USUARIO`:
```bat
git remote add origin https://github.com/TU_USUARIO/practica-git-telco.git
git push -u origin main
```
Si GitHub solicita autenticación, utiliza el navegador o el método de autenticación que GitHub Desktop/Git Credential Manager ofrezca. No compartas contraseñas ni tokens.

## Entrega
Incluye capturas de:
1. `git --version`.
2. `git status` después del primer commit.
3. Historial con `git log --oneline`.
4. Rama `mejora-documentacion` y su integración en `main`.
5. Repositorio en GitHub, si realizaste el paso opcional.

Responde brevemente:
- ¿Qué diferencia hay entre `git add` y `git commit`?
- ¿Qué información muestra `git status`?
- ¿Para qué sirve una rama?
- ¿Qué diferencia hay entre Git y GitHub?

Este proyecto utiliza Regresión Logística, Random Forest y SVM.

# Modelo SVM
Modelo de aprendizaje automatico supervizado y que se utiliza principalmente para tareas de clasificacion y regresion, funciona con un hiperplano que maximiza el margen en un espacio enrtre diferentes clases y es multidimensional.