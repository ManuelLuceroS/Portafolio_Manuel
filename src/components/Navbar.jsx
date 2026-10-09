import { useEffect, useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { Menu, X } from "lucide-react";
import { perfil } from "../data/portfolio";

const enlaces = [
  { href: "/#inicio", texto: "Inicio" },
  { href: "/#sobre-mi", texto: "Sobre mí" },
  { href: "/#experiencia", texto: "Experiencia" },
  { href: "/#proyectos", texto: "Proyectos" },
  { href: "/#habilidades", texto: "Habilidades" },
  { href: "/#educacion", texto: "Educación" },
  { href: "/#contacto", texto: "Contacto" },
];

export default function Navbar() {
  const [abierto, setAbierto] = useState(false);
  const ubicacion = useLocation();

  useEffect(() => {
    setAbierto(false);
  }, [ubicacion.pathname, ubicacion.hash]);

  return (
    <header className="navbar">
      <div className="contenedor navbar-contenido">
        <Link className="marca" to="/#inicio">
          {perfil.nombreCorto}
        </Link>

        <button
          className="menu-boton"
          type="button"
          aria-expanded={abierto}
          aria-label={abierto ? "Cerrar menú" : "Abrir menú"}
          onClick={() => setAbierto((valor) => !valor)}
        >
          {abierto ? <X size={20} /> : <Menu size={20} />}
        </button>

        <nav className={abierto ? "menu abierto" : "menu"} aria-label="Secciones del portafolio">
          {enlaces.map((enlace) => (
            <Link key={enlace.href} to={enlace.href}>
              {enlace.texto}
            </Link>
          ))}
        </nav>
      </div>
    </header>
  );
}
