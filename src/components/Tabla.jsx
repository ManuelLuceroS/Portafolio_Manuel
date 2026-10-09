export default function Tabla({ columnas, filas, clave }) {
  return (
    <div className="tabla-contenedor">
      <table>
        <thead>
          <tr>
            {columnas.map((columna) => (
              <th key={columna.clave} scope="col" className={columna.numero ? "num" : undefined}>
                {columna.titulo}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {filas.map((fila) => (
            <tr key={fila[clave]}>
              {columnas.map((columna) => (
                <td key={columna.clave} className={columna.numero ? "num" : undefined}>
                  {columna.formato ? columna.formato(fila[columna.clave]) : fila[columna.clave]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
