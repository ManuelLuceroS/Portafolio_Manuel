import { useEffect, useState } from "react";

export function useDatos(url) {
  const [datos, setDatos] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    let activo = true;

    fetch(url)
      .then((respuesta) => {
        if (!respuesta.ok) {
          throw new Error("No se encontró el archivo de resultados. Ejecuta el análisis en Python.");
        }
        return respuesta.json();
      })
      .then((json) => {
        if (activo) {
          setDatos(json);
        }
      })
      .catch((err) => {
        if (activo) {
          setError(err.message);
        }
      });

    return () => {
      activo = false;
    };
  }, [url]);

  return { datos, error };
}

export function EstadoDatos({ datos, error, children }) {
  if (error) {
    return <p className="mensaje-error">{error}</p>;
  }

  if (!datos) {
    return <p className="mensaje-carga">Cargando resultados calculados...</p>;
  }

  return children(datos);
}
