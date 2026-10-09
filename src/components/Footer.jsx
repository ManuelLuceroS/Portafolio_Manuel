import { perfil, contacto, enlaceActivo } from "../data/portfolio";

export default function Footer() {
  const linkedin = enlaceActivo(contacto.linkedin);

  return (
    <footer className="footer">
      <div className="contenedor footer-contenido">
        <p>{perfil.nombre}</p>
        <p>{perfil.ubicacion}</p>
        <a href={`mailto:${contacto.correo}`}>{contacto.correo}</a>
        {linkedin ? (
          <a href={contacto.linkedin.trim()} target="_blank" rel="noopener noreferrer">
            LinkedIn
          </a>
        ) : null}
      </div>
    </footer>
  );
}
