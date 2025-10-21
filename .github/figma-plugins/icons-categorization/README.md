# Icons Categorization Plugin

Este plugin de Figma automatiza la organización de iconos por categorías basándose en sus descripciones.

## Funcionamiento

El plugin lee la descripción de cada instancia seleccionada y busca el patrón:

```text
Category: [Nombre de la categoría]
```

Por ejemplo:

```text
Category: Actions and system

three-dimensional view, 3D perspective, 3D visualization, vista tridimensional, perspectiva 3D, 3D-Visualisierung
```

## Cómo usar

1. **Selecciona los iconos**: Selecciona todas las instancias de iconos que quieres organizar
2. **Ejecuta el plugin**: Ve a Plugins > Icons Categorization
3. **Resultado**: Los iconos se organizarán automáticamente en:
   - Bloques separados por categoría
   - Un título encima de cada categoría
   - Cuadrícula ordenada (8 iconos por fila por defecto)

## Características

- **Extracción automática de categorías**: Busca el patrón "Category:" en las descripciones
- **Organización en cuadrícula**: Los iconos se organizan en filas y columnas
- **Títulos de categoría**: Cada categoría tiene un título en negrita
- **Espaciado configurable**: Separación apropiada entre iconos y categorías
- **Manejo de casos especiales**: Los iconos sin categoría se agrupan en "Sin categoría"

## Configuración

Puedes modificar estas variables en el código para ajustar el layout:

- `ICONS_PER_ROW`: Número de iconos por fila (por defecto: 8)
- `SPACING_X`: Espaciado horizontal entre iconos (por defecto: 80px)
- `SPACING_Y`: Espaciado vertical entre iconos (por defecto: 80px)
- `CATEGORY_SPACING`: Espaciado entre categorías (por defecto: 120px)

## Requisitos

- Los elementos seleccionados deben ser instancias o componentes
- Las descripciones deben seguir el formato "Category: [nombre]"
- El plugin requiere acceso a la fuente "Inter Bold" para los títulos
