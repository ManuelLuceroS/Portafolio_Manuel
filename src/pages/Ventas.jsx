import { useEffect } from "react";
import { Link } from "react-router-dom";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  Line,
  LineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import Grafico from "../components/Grafico";
import KpiCard from "../components/KpiCard";
import Tabla from "../components/Tabla";
import {
  colores,
  estiloEje,
  estiloLeyenda,
  estiloTooltip,
  formatoMoneda,
  formatoNumero,
  formatoPorcentaje,
} from "../data/formato";
import { EstadoDatos, useDatos } from "../data/useDatos";

const columnasProductos = [
  { clave: "producto", titulo: "Producto" },
  { clave: "categoria", titulo: "Categoría" },
  { clave: "cantidad", titulo: "Unidades", numero: true, formato: formatoNumero },
  { clave: "ingresos", titulo: "Ingresos", numero: true, formato: formatoMoneda },
];

const columnasCategoria = [
  { clave: "categoria", titulo: "Categoría" },
  { clave: "ingresos", titulo: "Ingresos", numero: true, formato: formatoMoneda },
  { clave: "margen", titulo: "Margen", numero: true, formato: formatoMoneda },
  { clave: "margen_porcentaje", titulo: "% margen", numero: true, formato: formatoPorcentaje },
];

const columnasClientes = [
  { clave: "nombre", titulo: "Cliente" },
  { clave: "ciudad", titulo: "Ciudad" },
  { clave: "compras", titulo: "Compras", numero: true, formato: formatoNumero },
  { clave: "ingresos", titulo: "Ingresos", numero: true, formato: formatoMoneda },
];

const columnasMes = [
  { clave: "etiqueta", titulo: "Mes" },
  { clave: "ventas", titulo: "Ventas", numero: true, formato: formatoNumero },
  { clave: "ingresos", titulo: "Ingresos", numero: true, formato: formatoMoneda },
  { clave: "ticket_promedio", titulo: "Ticket", numero: true, formato: formatoMoneda },
  { clave: "ingresos_acumulados", titulo: "Acumulado", numero: true, formato: formatoMoneda },
];

function millones(valor) {
  return `${Math.round(valor / 1000000)} M`;
}

export default function Ventas() {
  const { datos, error } = useDatos("/datos/ventas.json");

  useEffect(() => {
    document.title = "Ventas | Manuel Lucero";
  }, []);

  return (
    <main id="contenido" className="pagina-dashboard">
      <div className="contenedor">
        <Link className="volver" to="/#proyectos">
          Volver a proyectos
        </Link>
        <p className="estado">Demostración</p>
        <h1>Análisis de ventas y clientes</h1>
        <p className="contexto">
          Una tienda quiere saber qué productos se venden más, qué categorías dejan más margen
          y cómo cambian los ingresos durante el año. Los clientes, productos y ventas son ficticios.
        </p>
        <p className="tecnologias-linea">SQL Server · Python · Pandas · Power BI</p>

        <EstadoDatos datos={datos} error={error}>
          {(info) => (
            <>
              <p className="advertencia">{info.advertencia}</p>

              <div className="kpi-grid">
                <KpiCard titulo="Ingresos" valor={formatoMoneda(info.kpis.ingresos)} />
                <KpiCard titulo="Ventas" valor={formatoNumero(info.kpis.ventas)} />
                <KpiCard titulo="Ticket promedio" valor={formatoMoneda(info.kpis.ticket_promedio)} />
                <KpiCard
                  titulo="Margen bruto"
                  valor={formatoPorcentaje(info.kpis.margen_porcentaje)}
                  detalle={formatoMoneda(info.kpis.margen_bruto)}
                />
              </div>
              <p className="nota">
                {formatoNumero(info.kpis.clientes_con_compra)} de {formatoNumero(info.kpis.clientes_maestro)} clientes
                del maestro compraron. {formatoNumero(info.kpis.clientes_recurrentes)} son recurrentes.{" "}
                {info.definicion_recurrente}
              </p>

              <div className="graficos">
                <Grafico titulo="Ventas mensuales" nota="El eje muestra millones de pesos. El tooltip conserva el valor completo." ancho>
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={info.mensual}>
                      <CartesianGrid stroke="#334155" strokeDasharray="3 3" />
                      <XAxis dataKey="etiqueta" tick={estiloEje} />
                      <YAxis tick={estiloEje} tickFormatter={millones} width={48} />
                      <Tooltip contentStyle={estiloTooltip} formatter={(valor) => formatoMoneda(valor)} />
                      <Line
                        type="monotone"
                        dataKey="ingresos"
                        name="Ingresos"
                        stroke="#22D3EE"
                        strokeWidth={2}
                        dot={false}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </Grafico>

                <Grafico titulo="Top 10 productos por unidades" alto ancho>
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={info.top_productos} layout="vertical" margin={{ left: 8, right: 12 }}>
                      <CartesianGrid stroke="#334155" strokeDasharray="3 3" />
                      <XAxis type="number" tick={estiloEje} />
                      <YAxis type="category" dataKey="producto" tick={estiloEje} width={168} />
                      <Tooltip contentStyle={estiloTooltip} formatter={formatoNumero} />
                      <Bar dataKey="cantidad" name="Unidades" fill="#3B82F6" radius={[0, 4, 4, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </Grafico>

                <Grafico titulo="Ingresos por categoría">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={info.por_categoria}
                        dataKey="ingresos"
                        nameKey="categoria"
                        outerRadius={95}
                        stroke="#0B1120"
                      >
                        {info.por_categoria.map((categoria, indice) => (
                          <Cell key={categoria.categoria} fill={colores[indice % colores.length]} />
                        ))}
                      </Pie>
                      <Tooltip contentStyle={estiloTooltip} formatter={(valor) => formatoMoneda(valor)} />
                      <Legend wrapperStyle={estiloLeyenda} />
                    </PieChart>
                  </ResponsiveContainer>
                </Grafico>

                <Grafico titulo="Margen porcentual por categoría">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={info.por_categoria}>
                      <CartesianGrid stroke="#334155" strokeDasharray="3 3" />
                      <XAxis dataKey="categoria" tick={estiloEje} interval={0} angle={-28} textAnchor="end" height={72} />
                      <YAxis tick={estiloEje} domain={[0, "auto"]} unit="%" width={48} />
                      <Tooltip contentStyle={estiloTooltip} formatter={(valor) => formatoPorcentaje(valor)} />
                      <Bar dataKey="margen_porcentaje" name="% margen" fill="#22D3EE" radius={[4, 4, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </Grafico>
              </div>

              <h2>Ranking de productos</h2>
              <Tabla columnas={columnasProductos} filas={info.top_productos} clave="producto" />

              <h2>Ventas por categoría</h2>
              <Tabla columnas={columnasCategoria} filas={info.por_categoria} clave="categoria" />

              <h2>Clientes con mayores compras</h2>
              <Tabla columnas={columnasClientes} filas={info.top_clientes} clave="nombre" />

              <h2>Detalle mensual</h2>
              <Tabla columnas={columnasMes} filas={info.mensual} clave="mes" />

              <h2>Lectura del análisis</h2>
              <p>{info.explicacion}</p>
              <ul className="formulas">
                {info.formulas.map((formula) => (
                  <li key={formula.nombre}>
                    <strong>{formula.nombre}.</strong> {formula.expresion}
                  </li>
                ))}
              </ul>

              <h2>Conclusiones</h2>
              <ul className="conclusiones">
                {info.conclusiones.map((texto) => (
                  <li key={texto}>{texto}</li>
                ))}
              </ul>
              <p className="nota">{info.fuente}</p>
            </>
          )}
        </EstadoDatos>
      </div>
    </main>
  );
}
