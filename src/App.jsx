import { useEffect } from "react";
import { Route, Routes, useLocation } from "react-router-dom";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import Home from "./pages/Home";
import Calidad from "./pages/Calidad";
import Ventas from "./pages/Ventas";
import Operaciones from "./pages/Operaciones";

function ScrollArriba() {
  const ubicacion = useLocation();

  useEffect(() => {
    if (ubicacion.hash) {
      const destino = document.querySelector(ubicacion.hash);
      if (destino) {
        destino.scrollIntoView();
        return;
      }
    }
    window.scrollTo(0, 0);
  }, [ubicacion.pathname, ubicacion.hash]);

  return null;
}

function NoEncontrada() {
  return (
    <main id="contenido" className="contenedor pagina-simple">
      <h1>Página no encontrada</h1>
      <p>Esa ruta no existe en el portafolio.</p>
    </main>
  );
}

export default function App() {
  return (
    <>
      <ScrollArriba />
      <a className="saltar" href="#contenido">
        Saltar al contenido
      </a>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/proyectos/calidad" element={<Calidad />} />
        <Route path="/proyectos/ventas" element={<Ventas />} />
        <Route path="/proyectos/operaciones" element={<Operaciones />} />
        <Route path="*" element={<NoEncontrada />} />
      </Routes>
      <Footer />
    </>
  );
}
