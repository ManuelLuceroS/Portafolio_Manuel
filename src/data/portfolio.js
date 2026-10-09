export const perfil = {
  nombre: "Manuel Enrique Lucero Suárez",
  nombreCorto: "Manuel Lucero",
  titulo: "Analista de Datos | Business Intelligence | Desarrollador de Software",
  tituloCorto: "Analista de Datos y Desarrollador de Software",
  ubicacion: "El Rosal, Cundinamarca, Colombia",
  saludo: "Hola, soy Manuel Lucero.",
  descripcion: [
    "Transformo datos en información útil y desarrollo soluciones tecnológicas que optimizan procesos.",
    "Cuento con experiencia en Power BI, SQL, Python, Excel y desarrollo de aplicaciones, combinando análisis de datos, automatización y programación para resolver necesidades reales de negocio.",
  ],
  cv: "/cv/CV-Manuel-Lucero.pdf",
};

export const indicadores = [
  { valor: "+20", detalle: "reportes desarrollados" },
  { valor: "3", detalle: "experiencias profesionales" },
  { valor: "Python, SQL y Power BI", detalle: "" },
  { valor: "Desarrollo de aplicaciones", detalle: "" },
];

export const enfoques = [
  "Análisis de datos",
  "Desarrollo de software",
  "Automatización",
  "Bases de datos",
  "Business Intelligence",
];

export const contacto = {
  correo: "manuelsuarez292005@gmail.com",
  // Pega aquí la URL completa cuando tengas el perfil publicado.
  github: "",
  linkedin: "https://www.linkedin.com/in/manuel-lucero-desarollo-analisis",
};

export const experiencia = [
  {
    cargo: "Analista de Datos",
    empresa: "High Control Group",
    periodo: "Agosto 2025 - Julio 2026",
    lugar: "El Rosal, Colombia",
    descripcion:
      "Participé en la transformación y gestión de información empresarial mediante soluciones de análisis de datos, automatización y reportes.",
    logros: [
      "Elaboración y mantenimiento de más de 20 reportes ejecutivos, operativos y específicos para clientes.",
      "Creación de dashboards en Power BI para visualizar indicadores de calidad, producción y gestión.",
      "Automatización de reportes mediante macros de Excel que consultaban bases de datos SQL y organizaban fotografías.",
      "Digitalización de procesos mediante formularios que facilitaron el acceso a información anteriormente registrada en formatos físicos.",
      "Gestión de usuarios y validación de datos en bases de datos utilizadas por aplicaciones empresariales.",
      "Resolución de inconsistencias y problemas de actualización de información.",
    ],
    tecnologias: ["Power BI", "SQL Server", "DAX", "Power Query", "Excel", "VBA", "Power BI Service"],
  },
  {
    cargo: "Analista de Datos",
    empresa: "Gnosis Consultores LLC",
    proyecto: "Supercanas",
    periodo: "Febrero 2025 - Julio 2025",
    lugar: "Remoto",
    descripcion:
      "Participación en el proyecto Supercanas, una plataforma digital orientada a la formación y acompañamiento de emprendedores mayores de 55 años, dentro del sector conocido como Silver Economy.",
    logros: [
      "Apoyo en el análisis y organización de información del proyecto.",
      "Organización de datos relacionados con actividades y participantes.",
      "Apoyo a la consulta y seguimiento de información de la plataforma.",
    ],
    enlace: {
      href: "https://www.supercanas.com/",
      texto: "Conocer Supercanas",
    },
  },
  {
    cargo: "Desarrollador Junior",
    empresa: "C.I. Sunshine Bouquet S.A.S.",
    periodo: "Julio 2024 - Enero 2025",
    lugar: "Etapa productiva SENA",
    descripcion:
      "Participé en el desarrollo e implementación de una aplicación móvil y web para gestionar procesos académicos relacionados con aprendices, instructores y comités.",
    logros: [
      "Desarrollo de interfaces móviles utilizando Flutter y Dart.",
      "Integración con servicios backend desarrollados en Python y Django.",
      "Implementación de consultas y actualización de información mediante APIs.",
      "Generación de documentos PDF y Excel.",
      "Centralización de información académica para facilitar consultas y seguimiento.",
      "Adaptación de funcionalidades para procesos de cancelación de matrícula y condicionamiento de aprendices.",
    ],
    tecnologias: ["Flutter", "Dart", "Python", "Django", "APIs REST", "PDF", "Excel"],
  },
];

export const proyectos = [
  {
    id: "reportes",
    nombre: "Sistema de reportes de gestión y calidad",
    categoria: "Business Intelligence",
    descripcion:
      "Solución de análisis de datos orientada al seguimiento de indicadores operativos, auditorías, rankings, revisiones de calidad y análisis de no conformidades. Permite comparar resultados por periodos, identificar tendencias y facilitar la consulta de información.",
    tecnologias: ["Power BI", "SQL", "DAX", "Power Query"],
    etiquetas: ["Business Intelligence", "Dashboards", "SQL", "Análisis de datos"],
    icono: "reportes",
  },
  {
    id: "automatizacion",
    nombre: "Automatización de reportes empresariales",
    categoria: "Automatización",
    descripcion:
      "Solución desarrollada mediante macros de Excel para consultar información desde bases de datos SQL, organizar fotografías y facilitar la generación de reportes. El objetivo fue reducir actividades manuales y simplificar la preparación de información operativa.",
    tecnologias: ["Excel", "VBA", "SQL Server"],
    icono: "automatizacion",
  },
  {
    id: "supercanas",
    nombre: "Supercanas",
    categoria: "Análisis de datos / Silver Economy",
    descripcion:
      "Proyecto digital orientado al acompañamiento de emprendedores mayores de 55 años. Participé en actividades relacionadas con la organización y consulta de información para apoyar el seguimiento del proyecto.",
    etiquetas: ["Análisis de datos", "Silver Economy"],
    externo: "https://www.supercanas.com/",
    accion: "Visitar proyecto",
    icono: "supercanas",
  },
  {
    id: "academico",
    nombre: "Sistema de gestión académica",
    categoria: "Desarrollo de software",
    descripcion:
      "Aplicación móvil y web implementada para centralizar información relacionada con aprendices, instructores y comités. Incluye consultas de información, seguimiento de procesos y generación de documentos PDF y Excel.",
    tecnologias: ["Flutter", "Dart", "Python", "Django", "APIs REST"],
    icono: "academico",
  },
  {
    id: "dannys",
    nombre: "Catálogo digital Danny's",
    categoria: "Desarrollo de aplicaciones",
    descripcion:
      "Catálogo digital con gestión de productos, categorías, carrito de compras y envío de pedidos mediante WhatsApp. Incluye funcionalidades para la administración de productos.",
    tecnologias: ["Flutter", "Firebase", "Firestore", "Cloudinary"],
    icono: "dannys",
  },
];

export const laboratorio = [
  {
    id: "calidad",
    nombre: "Análisis de calidad y no conformidades",
    categoria: "Demostración",
    estado: "Datos ficticios",
    descripcion:
      "Ejercicio con datos ficticios de una floricultora. Revisa causas frecuentes y cómo cambia la no conformidad entre semanas.",
    tecnologias: ["Python", "Pandas", "SQL", "Power BI"],
    ruta: "/proyectos/calidad",
    accion: "Ver proyecto",
    icono: "calidad",
  },
  {
    id: "ventas",
    nombre: "Análisis de ventas y clientes",
    categoria: "Demostración",
    estado: "Datos ficticios",
    descripcion:
      "Ejercicio con datos ficticios de una tienda. Calcula ingresos, ticket promedio, categorías y clientes que más compran.",
    tecnologias: ["SQL Server", "Python", "Pandas", "Power BI"],
    ruta: "/proyectos/ventas",
    accion: "Ver proyecto",
    icono: "ventas",
  },
  {
    id: "operaciones",
    nombre: "Análisis de indicadores operativos",
    categoria: "Demostración",
    estado: "Datos ficticios",
    descripcion:
      "Ejercicio con datos ficticios para comparar el cumplimiento de metas entre áreas, semanas y meses.",
    tecnologias: ["Python", "SQL", "Power BI", "Excel"],
    ruta: "/proyectos/operaciones",
    accion: "Ver proyecto",
    icono: "operaciones",
  },
];

export const habilidades = [
  {
    grupo: "Análisis de datos",
    items: ["Power BI", "SQL", "DAX", "Power Query", "Modelado de datos", "Excel"],
  },
  {
    grupo: "Programación",
    items: ["Python", "Dart", "Flutter", "Django", "APIs REST"],
  },
  {
    grupo: "Bases de datos",
    items: ["SQL Server", "Consultas SQL", "Validación de datos", "Transformación de datos", "Firebase / Firestore"],
  },
  {
    grupo: "Herramientas",
    items: ["Power BI Service", "Gateway", "Excel VBA", "Git", "GitHub", "Cloudinary"],
  },
];

export const educacion = [
  {
    titulo: "Ingeniería de Sistemas",
    institucion: "Universidad Nacional Abierta y a Distancia (UNAD)",
    periodo: "2025 - Actualidad",
    detalle: "En curso · Quinto semestre",
    enCurso: true,
  },
  {
    titulo: "Tecnólogo en Análisis y Desarrollo de Software",
    institucion: "SENA",
    periodo: "2023 - 2024",
  },
  {
    titulo: "Técnico en Programación de Software",
    institucion: "SENA",
    periodo: "2021 - 2022",
  },
];

export function enlaceActivo(url) {
  return typeof url === "string" && url.trim().startsWith("http");
}
