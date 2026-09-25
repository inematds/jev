# Jev Decision Lab

**Idiomas:** [Português](README.md) · [English](README.en.md) · [Español](README.es.md)

![Jev Decision Lab — más funciones, uso sencillo: 20 casos prácticos, experimentos y comparación](capa/novos-recursos-v1.2.1.png)

**v1.8.1** · Un laboratorio para formular, probar y comparar decisiones de IA, con una interfaz sencilla y funciones avanzadas cuando las necesites.

[Abrir laboratorio](https://inematds.github.io/jev/app/) · [Guía de uso](https://inematds.github.io/jev/guia/) · [Curso en portugués](https://inematds.github.io/jev-curso/)

[Acervo Jev en Eventos INEMA](https://eventos.inema.pro/jev/es/) — proyecto, curso y paquetes reunidos en una página, con presentación en portugués, inglés y español.

Este README está traducido al español. La interfaz, la documentación enlazada del proyecto, el curso y el contenido de los ejemplos siguen en portugués. Los comandos, las rutas y los identificadores conservan su escritura original para que puedas ejecutarlos tal como aparecen.

**Referencia oficial de modelos, precios, modalidades y límites:** https://docs.typesafe.ai/models

**Lee también: [Exageraciones, dudas y límites de Jev](docs/07-exageros-e-duvidas.md).** El documento distingue entre capacidades documentadas, hipótesis, extrapolaciones y evidencia todavía necesaria.

## Incorpóralo a tu proyecto

La carpeta **[pacotes/](pacotes/README.md)** reúne **18 paquetes por área**, una integración Python, la skill `jev-integrar` y recetas de uso. Empieza sin conexión con `python3 -m pacotes.executar atendimento`. Para tu backend, consulta [cómo integrar Jev en tus sistemas](pacotes/INTEGRACAO.md). Cada paquete explica qué funciona y qué sigue dependiendo de una integración.

## Nuevos flujos prácticos

Ahora hay **18 paquetes reutilizables**: los diez originales más **bandeja de entrada, comentarios de YouTube, comunidades, reuniones, selección de clips por transcripción, notas, curación del feed y alojamiento × perfiles de viajeros**. Los nuevos paquetes combinan Choice, Noul y Score; sus fixtures son ficticias, sin benchmark real. El paquete de viajes evalúa cada anuncio una sola vez y cruza las respuestas con doce perfiles mediante una regla (`python3 -m pacotes.cruzamento viagens --preco 420`).

```bash
python3 -m pacotes.executar reunioes
python3 -m pacotes.qualidade reunioes
python3 -m pacotes.lote reunioes data/reunioes-eventos.jsonl
```

Los dos primeros comandos demuestran el ejemplo y sus métricas simuladas. El tercero muestra una vista previa sin API. Con `--live`, el ejecutor procesa JSONL, admite hasta cuatro workers y retoma resultados guardados. La evaluación por pregunta mide acierto, Brier o error de Score según el tipo. **[Instrucciones, integración y límites](docs/11-fluxos-praticos.md)**. No hay recopilación de datos de plataformas ni ejecución automática de acciones.

## Jev real mediante OpenRouter

Soporte para **`~typesafe/jev-latest`**, confirmado en la Decisions API. Configura `OPENROUTER_API_KEY` en el backend y ejecuta:

```bash
python3 -m pacotes.executar atendimento --live --provider openrouter
```

Los diez paquetes originales se probaron con inferencia real: diez respuestas sin fallos y diez clasificaciones esperadas en ejemplos ficticios. Es una prueba de integración, no un benchmark independiente. [Configuración y código para tu sistema](docs/10-openrouter.md) · [Informe medido](reports/openrouter-smoke.json).

## Uso en Codex, Claude Code y openpcbotv3

- **Codex:** `$jev-decidir` seguido del contexto y las alternativas.
- **Claude Code:** `/jev-decidir` seguido del contexto y las alternativas.
- **openpcbotv3:** `/jev observar` compara ruta, agente y skill; `/jev` muestra el resultado y `/jev off` desactiva la observación. Integración nativa mediante el gateway, con control del presupuesto y registro de costes.

[Instalación y ejemplos de la skill](pacotes/skills/jev-decidir/README.md) · [Integración en el bot](https://github.com/inematds/openpcbotv3/blob/main/docs/JEV.md). La consulta directa usa el cliente de este repositorio; el bot conserva su propio gateway y enrutador, con Jev en modo de observación.

## Empieza en un minuto

En el sitio público, elige uno de los **20 casos originales**, examina el contexto y los criterios y explora la respuesta didáctica. Puedes editar preguntas, importar/exportar JSON y estimar costes sin registrar una clave.

Para abrirlo en tu ordenador:

```bash
git clone https://github.com/inematds/jev.git
cd jev
python3 -m jev_lab serve
```

Abre `http://127.0.0.1:8765`. Requiere Python 3.10+; el núcleo utiliza únicamente la biblioteca estándar. No necesitas instalar un framework, una base de datos ni un servicio de colas.

## Funciones disponibles

| Función | Qué puedes hacer |
|---|---|
| 20 casos con búsqueda | Explorar atención al cliente, evidencias, agentes, skills, código, logs y más |
| Choice, Noul y Score | Elegir alternativas, medir la probabilidad de sí o usar rúbricas ordenadas |
| Varias preguntas sobre el mismo contexto | Separar cola, urgencia, suficiencia e intenciones |
| Contexto textual o JSON | Representar documentos, catálogos y estados estructurados |
| Importación y exportación | Llevar solicitudes a la CLI y guardar resultados con procedencia |
| Política didáctica | Observar cómo los umbrales y la abstención afectan a la revisión; no se ejecuta ninguna acción externa |
| Coste total estimado | Añadir alternativas de respaldo, revisión humana e infraestructura al coste de entrada |
| Experimentos por lotes | Ejecutar reglas, Jev directo, modo híbrido o replay sobre un conjunto de datos etiquetado |
| Comparación y métricas | Examinar macro-F1, confusión, cobertura, precisión de las predicciones aceptadas, Brier/ECE, latencia y coste desconocido |
| Visor de informes | Abrir report.json en el navegador e identificar errores para investigar |

Las respuestas del sitio son **simulaciones originales**, claramente identificadas. Editar el contexto, el tipo, las opciones o la pregunta desactiva la respuesta de ejemplo anterior (fixture). La página pública no consulta ninguna API; en el servidor local, la consulta real requiere una clave.

## Los 20 casos

Los diez iniciales: afirmaciones, atención al cliente, contratos, cambios en conversaciones por correo, modelos, verificación de pasos, agentes, navegador mediante candidatos, revisión clínica ficticia y alertas financieras ficticias.

Los diez adicionales: **skills, calidad de comentarios, filtro de evidencias, triaje compuesto, intenciones simultáneas, fechas mediante candidatos, gravedad de logs, datos personales minimizados, tema frente a intención y revisión de diff**.

Cada caso incluye estado, preguntas, fixture, explicación y siguiente paso. Los casos de herramientas/navegador sugieren candidatos; no controlan agentes, navegadores ni dispositivos. Los ejemplos sensibles permanecen supervisados.

## Terminal: del ejemplo al experimento

```bash
# Listar y exportar un ejemplo
python3 -m jev_lab cases
python3 -m jev_lab cases --id triagem-composta --out exemplos/minha-requisicao.json

# Validar el contrato sin consumir la API
python3 -m jev_lab validate exemplos/triagem-composta-request.json

# Consultar Jev cuando se disponga de acceso
python3 -m jev_lab ask exemplos/triagem-composta-request.json

# Experimento reproducible sin clave
python3 -m jev_lab experiment data/tickets-sinteticos.jsonl --out runs/regras

# Experimento con Jev real
python3 -m jev_lab experiment data/tickets-sinteticos.jsonl --provider jev --out runs/jev

# Comparar dos ejecuciones sobre el mismo conjunto de datos
python3 -m jev_lab compare runs/regras/report.json runs/jev/report.json
```

El comando anterior `batch` sigue disponible. Para plantillas de otras tareas, repetibilidad, modo híbrido e importación de resultados de LLM, consulta **[Experimentos reproducibles](docs/08-experimentos.md)**. No hay adaptador LLM en vivo: la comparación externa utiliza replay con hash de la solicitud y procedencia declarada.

## Configuración local

El cliente utiliza `OPENROUTER_API_KEY` con OpenRouter y `TYPESAFE_API_KEY` con TypeSafe directamente. Carga la clave desde el entorno o, durante la ejecución, desde `~/projetos/openpcbotv2/.env` y `~/projetos/wifi/.env`. No copia la clave ni la envía al navegador. Sin acceso, los ejemplos, la exportación, la calculadora y las reglas siguen funcionando; las llamadas reales registran un fallo explícito.

El servidor escucha únicamente en loopback, valida el origen y sirve archivos permitidos. Serializa las consultas al proveedor. No es un backend público multiusuario. La aplicación acepta descripciones textuales, hasta 30 preguntas y 100 KB por payload; estos dos últimos límites son locales, no límites anunciados de Jev. Score utiliza entre 2 y 10 niveles y exige una `legend` correspondiente en la respuesta.

## Evidencia y límites

- Se volvió a ejecutar la referencia de reglas: **20/24 aciertos (83,33 %)**, macro-F1 **0,84235**, en tickets ficticios. [Informe de reglas](reports/experimento-regras/report.json).
- Hay un [replay didáctico](data/replay-didatico.jsonl) con errores intencionados y coste/latencia desconocidos. La [comparación de ejemplo](reports/comparacao-didatica.json) es un ejercicio, no un benchmark de Jev.
- Las pruebas verifican contratos, presupuesto, fallos, duplicados, replay, repetibilidad y políticas. Las verificaciones del navegador cubren los 20 casos, la edición, los tipos, la importación/exportación y la lectura de informes.
- **Hay una prueba de integración real mediante OpenRouter, pero no un benchmark independiente.** La suite automatizada utiliza respuestas controladas; el informe separado registra las diez consultas reales. La calidad en portugués y la calibración aún requieren evaluación con referencias humanas sobre datos independientes.
- No hay envío de mensajes, pagos, merge, diagnóstico ni ejecución de herramientas. La clasificación no concede permisos.

## Documentación

- [Usar Jev mediante OpenRouter](docs/10-openrouter.md)
- [Exageraciones, dudas y límites](docs/07-exageros-e-duvidas.md)
- [Experimentos y formato de replay](docs/08-experimentos.md)
- [Qué se incorporó y qué depende de evidencia](docs/09-evolucao.md)
- [Análisis conceptual](docs/01-analise.md) · [Diez aplicaciones iniciales](docs/02-aplicacoes.md)
- [Plan original](docs/03-plano-aplicacao.md) · [Protocolo de evaluación](docs/04-avaliacao.md) · [Costes](docs/05-custos.md)
- [Curso: 36 lecciones y 12 laboratorios](https://inematds.github.io/jev-curso/)
- [Modelos oficiales](https://docs.typesafe.ai/models) · [API oficial](https://docs.typesafe.ai/api)

## Desarrollo y publicación

```bash
python3 -m unittest discover -s tests -v
python3 scripts/build_site.py
```

Las pruebas de navegador de `tests/browser.cjs` utilizan Playwright solo durante el desarrollo. Instálalo en el entorno de pruebas con `npm install --no-save --package-lock=false playwright` y `npx playwright install chromium`; la aplicación no necesita esta dependencia. `BASE_URL`, `GUIDE_URL` y `SCREENSHOT_DIR` permiten elegir los servidores y el directorio de capturas de la prueba. El build publica una lista explícita: `app/`, `guia/`, `capa/` y la entrada del sitio. La documentación pública permanece en el repositorio.

**Las transcripciones y los materiales recibidos permanecen únicamente en local**, ignorados por Git y excluidos del build. Los informes operativos van en `runs/`, también ignorada. Los documentos públicos son originales, con referencias oficiales. Consulta el [changelog](CHANGELOG.md).

## Plan del piloto y puntuación compuesta

[Planifica una decisión, define casos límite y combina rúbricas Score](docs/12-piloto-e-composicao.md) (portugués). `pacotes.composicao.compor` valida los datos y calcula un índice ponderado; no representa confianza ni autorización. El [curso HTML v2](https://inematds.github.io/jev-curso/) ofrece 36 lecciones, progreso y un plan personal (portugués).

## Pendientes y alternativa local

[Pendientes confirmados](tasks/current.md) · [Análisis de Laya para comparar con Jev y realizar un piloto en el bot v3](docs/13-analise-laya.md) (portugués). La integración con Laya está propuesta, todavía no implementada.

### Referencias de Laya

Laya es un candidato local para un piloto comparativo. El análisis y las referencias están disponibles; el adaptador de Jev y la integración con el bot siguen pendientes.

[Laya INEMA](https://github.com/inematds/laya) · [Código original](https://github.com/NandhaKishorM/laya) · [Modelos y ficha del modelo](https://huggingface.co/convaiinnovations/laya) · [Laya en Eventos](https://eventos.inema.pro/jev/#laya)
