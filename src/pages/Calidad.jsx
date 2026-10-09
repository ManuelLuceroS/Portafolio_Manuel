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
import { colores, estiloEje, estiloLeyenda, estiloTooltip, formatoNumero, formatoPorcentaje } from "../data/formato";
import { EstadoDatos, useDatos } from "../data/useDatos";

const columnasFinca = [
  { clave: "finca", titulo: "Finca" },
  { clave: "revisados", titulo: "Revisados", numero: true, formato: formatoNumero },
  { clave: "no_conformes", titulo: "No conformes", numero: true, formato: formatoNumero },
  { clave: "porcentaje", titulo: "% no conformidad", numero: true, formato: formatoPorcentaje },
];

const columnasMes = [
  { clave: "etiqueta", titulo: "Mes" },
  { clave: "revisados", titulo: "Revisados", numero: true, formato: formatoNumero },
  { clave: "no_conformes", titulo: "No conformes", numero: true, formato: formatoNumero },
  { clave: "porcentaje", titulo: "% no conformidad", numero: true, formato: formatoPorcentaje },
];

function tooltipPorcentaje(valor) {
  return formatoPorcentaje(valor);
}

export default function Calidad() {
  const { datos, error } = useDatos("/datos/calidad.json");

  useEffect(() => {
    document.title = "Calidad | Manuel Lucero";
  }, []);

  return (
    <main id="contenido" className="pagina-dashboard">
      <div className="contenedor">
        <Link className="volver" to="/#proyectos">
          Volver a proyectos
        </Link>
        <p className="estado">Demostración</p>
        <h1>Análisis de calidad y no conformidades</h1>
        <p className="contexto">
          Una empresa del sector floricultor necesita ver qué problemas se repiten en los ramos
          y cómo cambia la no conformidad entre fincas, variedades y semanas. Los datos son
          ficticios y no pertenecen a una empresa real.
        </p>
        <p className="tecnologias-linea">Python · Pandas · SQL · Power BI</p>

        <EstadoDatos datos={datos} error={error}>
          {(info) => (
            <>
              <p className="advertencia">{info.advertencia}</p>

              <div className="kpi-grid">
                <KpiCard titulo="Ramos revisados" valor={formatoNumero(info.kpis.ramos_revisados)} />
                <KpiCard titulo="Ramos no conformes" valor={formatoNumero(info.kpis.ramos_no_conformes)} />
                <KpiCard
                  titulo="No conformidad"
                  valor={formatoPorcentaje(info.kpis.porcentaje_no_conformidad)}
                />
                <KpiCard titulo="Inspecciones" valor={formatoNumero(info.kpis.inspecciones)} />
              </div>

              <div className="graficos">
                <Grafico
                  titulo="Evolución semanal"
                  nota="Cada punto usa la semana ISO y el año, para no mezclar semanas de años distintos. La semana 1 tiene menos días porque el archivo empieza el 2 de enero."
                  ancho
                >
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={info.evolucion_semanal}>
                      <CartesianGrid stroke="#334155" strokeDasharray="3 3" />
                      <XAxis dataKey="etiqueta" tick={estiloEje} interval={3} />
                      <YAxis tick={estiloEje} domain={[0, "auto"]} unit="%" width={48} />
                      <Tooltip
                        contentStyle={estiloTooltip}
                        formatter={tooltipPorcentaje}
                        labelFormatter={(_, items) => items?.[0]?.payload?.clave || ""}
                      />
                      <Line
                        type="monotone"
                        dataKey="porcentaje"
                        name="% no conformidad"
                        stroke="#22D3EE"
                        strokeWidth={2}
                        dot={false}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </Grafico>

                <Grafico titulo="No conformidad por finca">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={info.por_finca}>
                      <CartesianGrid stroke="#334155" strokeDasharray="3 3" />
                      <XAxis dataKey="finca" tick={estiloEje} interval={0} angle={-28} textAnchor="end" height={72} />
                      <YAxis tick={estiloEje} domain={[0, "auto"]} unit="%" width={48} />
                      <Tooltip contentStyle={estiloTooltip} formatter={tooltipPorcentaje} />
                      <Bar dataKey="porcentaje" name="% no conformidad" fill="#3B82F6" radius={[4, 4, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </Grafico>

                <Grafico titulo="Causas de no conformidad" nota="El porcentaje es sobre los ramos no conformes, no sobre los revisados.">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie data={info.causas} dataKey="ramos" nameKey="causa" outerRadius={95} stroke="#0B1120">
                        {info.causas.map((causa, indice) => (
                          <Cell key={causa.causa} fill={colores[indice % colores.length]} />
                        ))}
                      </Pie>
                      <Tooltip contentStyle={estiloTooltip} formatter={formatoNumero} />
                      <Legend wrapperStyle={estiloLeyenda} />
                    </PieChart>
                  </ResponsiveContainer>
                </Grafico>

                <Grafico titulo="No conformidad por variedad">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={info.por_variedad}>
                      <CartesianGrid stroke="#334155" strokeDasharray="3 3" />
                      <XAxis dataKey="variedad" tick={estiloEje} interval={0} angle={-28} textAnchor="end" height={72} />
                      <YAxis tick={estiloEje} domain={[0, "auto"]} unit="%" width={48} />
                      <Tooltip contentStyle={estiloTooltip} formatter={tooltipPorcentaje} />
                      <Bar dataKey="porcentaje" name="% no conformidad" fill="#22D3EE" radius={[4, 4, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </Grafico>

                <Grafico titulo="Comparación mensual">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={info.comparacion_mensual}>
                      <CartesianGrid stroke="#334155" strokeDasharray="3 3" />
                      <XAxis dataKey="etiqueta" tick={estiloEje} />
                      <YAxis tick={estiloEje} domain={[0, "auto"]} unit="%" width={48} />
                      <Tooltip contentStyle={estiloTooltip} formatter={tooltipPorcentaje} />
                      <Bar dataKey="porcentaje" name="% no conformidad" fill="#3B82F6" radius={[4, 4, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </Grafico>
              </div>

              <h2>Resultados por finca</h2>
              <Tabla columnas={columnasFinca} filas={info.por_finca} clave="finca" />

              <h2>Resultados por mes</h2>
              <Tabla columnas={columnasMes} filas={info.comparacion_mensual} clave="mes" />

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
