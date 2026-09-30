# AI_Project — Sistema de recomendación con GitHub Copilot

**Asignatura:** ETVI02 — Tendencias emergentes en IA · Unidad 3, Semana 8
**Actividad formativa:** GitHub Copilot
**Estudiante:** Victor Miguel González González
**Fecha:** 30/09/2026

---

## 1. Descripción del proyecto

Este repositorio contiene un **sistema de recomendación de películas** escrito en Python. El código se desarrolló con asistencia de IA y se analizó con **GitHub Copilot Chat** dentro de Visual Studio Code.

El sistema aplica **filtrado colaborativo**, una de las técnicas de IA más usadas en plataformas como Netflix, Spotify o Amazon:

| Enfoque | Idea | Método |
|---|---|---|
| Basado en usuarios | "A usuarios parecidos a ti les gustó X" | `recommend_user_based()` |
| Basado en ítems | "X se parece a lo que ya te gustó" | `recommend_item_based()` |

Para medir el parecido se usa la **similitud del coseno** sobre las valoraciones centradas en la media de cada usuario. Así, una nota baja cuenta como "no me gustó" y no como un "me gustó" más débil.

## 2. Requisitos

- Python 3.8 o superior (no necesita librerías externas)
- Visual Studio Code con la extensión **GitHub Copilot**
- Git

## 3. Cómo ejecutarlo

```bash
python recommendation_system.py
```

Salida de ejemplo (fragmento):

```
=== Ana ===
  Usuarios similares: Bruno (0.40), Felipe (0.36)
  Recomendación (usuarios): [('Blade Runner', 4.04), ('La La Land', 1.4), ('Coco', 1.19)]
  Recomendación (ítems):    [('Blade Runner', 4.21), ('La La Land', 1.63), ('Coco', 1.1)]
```

El número junto a cada película es la **nota que el sistema predice** (de 1 a 5). A Ana le gustan la ciencia ficción y las películas de Nolan, así que el sistema le recomienda *Blade Runner* con una nota alta y predice notas bajas para las demás.

---

## 4. Proceso seguido (paso a paso)

### Paso 1 — Crear la cuenta en GitHub y activar Copilot
Entré en <https://github.com/>, creé mi cuenta y validé el correo electrónico. En la sección de precios de GitHub Copilot elegí el plan **gratuito** (o el beneficio para estudiantes de GitHub Education).

![Registro en GitHub](capturas/paso1.png)

### Paso 2 — Crear el repositorio
Pulsé **New** y creé el repositorio `AI_Project` con visibilidad **pública**. Añadí un `README`, un `.gitignore` (plantilla Python) y una licencia **MIT**. Por último pulsé **Create repository**.

![Creación del repositorio](capturas/paso2.png)

### Paso 3 — Clonar el repositorio en Visual Studio Code
Cloné el repositorio en la carpeta Documentos y lo abrí en Visual Studio Code:

```bash
git clone https://github.com/vittoxd/AI_Project.git
cd AI_Project
code .
```

![Repositorio abierto en VS Code](capturas/paso3.png)

### Paso 4 — Usar GitHub Copilot con el código
Con el repositorio abierto, inicié sesión en VS Code con mi cuenta de GitHub y marqué la carpeta como de confianza. En modo restringido Copilot no funciona.

Luego abrí **Copilot Chat** (panel derecho), adjunté `recommendation_system.py` como contexto y le escribí esta petición:

```
Función que calcula la similitud del coseno entre dos diccionarios de valoraciones
def
```

Copilot revisó el archivo y, en lugar de generar una función duplicada, detectó que ya existía como `cosine_similarity(a, b)` y explicó qué hace.

![Copilot Chat analizando el código](capturas/paso4.png)

**Observaciones sobre Copilot:**
- **Entiende el contexto del proyecto:** no se limitó a responder la petición al pie de la letra. Leyó el archivo adjunto, reconoció que la función ya estaba implementada y respondió en español aunque su interfaz está en inglés.
- **Su explicación no fue del todo exacta:** dijo que la función "calcula el coseno usando las claves compartidas". Al comparar con el código vi que el producto punto sí usa solo las películas en común, pero las **normas se calculan con el vector completo** de cada usuario. Ese detalle es importante: hace que dos usuarios con muy pocas películas en común tengan una similitud baja. Copilot lo simplificó y, sin revisar el código, habría aceptado una descripción incompleta.
- **Requiere configuración previa:** para que funcionara tuve que iniciar sesión en VS Code y quitar el modo restringido de la carpeta. Antes de eso, el panel de Copilot no respondía.
- **Probar el programa también fue clave:** al ejecutarlo comprobé que las recomendaciones dependen mucho de los datos. Por ejemplo, a quienes les gusta la ciencia ficción el sistema les recomienda *Blade Runner* o *Interstellar* con notas superiores a 4.

### Paso 5 — Probar el programa
Ejecuté `python recommendation_system.py` y comprobé que las recomendaciones eran coherentes con los gustos de cada usuario.

![Ejecución del programa](capturas/paso5.png)

### Paso 6 — Commit y push
```bash
git add .
git commit -m "Agrega capturas de pantalla"
git push origin main
git log --oneline
```

![Commit y push](capturas/paso6.png)

---

## 5. Relación con las tendencias emergentes en IA

- **IA generativa aplicada a la programación:** Copilot usa modelos de lenguaje de gran tamaño (LLM) para convertir descripciones en lenguaje natural en código.
- **Sistemas de recomendación:** son una de las aplicaciones de IA con más impacto comercial y personalizan el contenido para cada usuario.
- **Programación asistida:** el desarrollador pasa de escribir cada línea a guiar, revisar y validar lo que propone la IA.

## 6. Conclusiones

GitHub Copilot es útil para entender código rápido: leyó el archivo del proyecto, reconoció qué funciones ya existían y las explicó en lenguaje natural en pocos segundos. Sin embargo, la actividad dejó claro que sus respuestas **no siempre son exactas**. Su descripción de la similitud del coseno omitía un detalle importante (las normas usan el vector completo), y solo lo noté al comparar la explicación con el código. Por eso Copilot funciona mejor como un asistente que como una fuente de verdad: el desarrollador sigue siendo responsable de leer, probar y validar lo que propone. Lo volvería a usar para explorar código desconocido, generar código repetitivo y resolver dudas rápidas, pero siempre comprobando sus respuestas.

## 7. Referencias

- GitHub. (s. f.). *GitHub Copilot Documentation*. <https://docs.github.com/en/copilot>
- GitHub. (s. f.). *Getting Started with GitHub Copilot*. <https://docs.github.com/en/copilot/getting-started-with-github-copilot>
