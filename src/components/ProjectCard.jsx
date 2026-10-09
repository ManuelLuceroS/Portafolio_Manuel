import { Link } from "react-router-dom";
import {
  ArrowRight,
  BarChart3,
  ClipboardList,
  FileSpreadsheet,
  GraduationCap,
  ShoppingBag,
  ShoppingCart,
  Users,
} from "lucide-react";

const iconos = {
  calidad: BarChart3,
  ventas: ShoppingCart,
  operaciones: ClipboardList,
  reportes: BarChart3,
  automatizacion: FileSpreadsheet,
  supercanas: Users,
  academico: GraduationCap,
  dannys: ShoppingBag,
};

export default function ProjectCard({ proyecto }) {
  const Icono = iconos[proyecto.icono] || BarChart3;
  const etiquetas = [
    ...new Set([...(proyecto.tecnologias || []), ...(proyecto.etiquetas || [])]),
  ];
  const textoBoton = proyecto.accion || "Ver proyecto";
  const externo = Boolean(proyecto.externo);
  const destino = proyecto.externo || proyecto.ruta;

  const titulo = destino ? (
    externo ? (
      <a href={proyecto.externo} target="_blank" rel="noopener noreferrer">
        {proyecto.nombre}
      </a>
    ) : (
      <Link to={proyecto.ruta}>{proyecto.nombre}</Link>
    )
  ) : (
    proyecto.nombre
  );

  return (
    <article className={destino ? "tarjeta-proyecto tarjeta-enlace" : "tarjeta-proyecto"}>
      <div className={`miniatura miniatura-${proyecto.id}`}>
        <Icono size={26} aria-hidden="true" />
        <span>{proyecto.estado || proyecto.categoria}</span>
      </div>
      <div className="tarjeta-cuerpo">
        <h3>{titulo}</h3>
        <p>{proyecto.descripcion}</p>
        {etiquetas.length > 0 ? (
          <ul className="tecnologias">
            {etiquetas.map((etiqueta) => (
              <li key={etiqueta}>{etiqueta}</li>
            ))}
          </ul>
        ) : null}
        {destino ? (
          <span className="boton boton-texto">
            {textoBoton}
            <ArrowRight size={16} aria-hidden="true" />
          </span>
        ) : null}
      </div>
    </article>
  );
}
