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
import { estiloEje, estiloLeyenda, estiloTooltip, formatoDecimal, formatoNumero, formatoPorcentaje } from "../data/formato";
import { EstadoDatos, useDatos } from "../data/useDatos";

const colorEstado = {
  Cumplida: "#3B82F6",
  Parcial: "#22D3EE",
  "No cumplida": "#64748B",
};

const columnasArea = [
  { clave: "area", titulo: "Área" },
  { clave: "unidad", titulo: "Unidad" },
  { clave: "actividades", titulo: "Actividades", numero: true, formato: formatoNumero },
  { clave: "cumplimiento", titulo: "Cumplimiento", numero: true, formato: formatoPorcentaje },
  {
    clave: "productividad",
    titulo: "Productividad",
    numero: true,
    formato: formatoDecimal,
  },
];

const columnasMes = [
  { clave: "etiqueta", titulo: "Mes" },
  { clave: "actividades", titulo: "Actividades", numero: true, formato: formatoNumero },
  { clave: "cumplimiento", titulo: "Cumplimiento", numero: true, formato: formatoPorcentaje },
];

export default function Operaciones() {
  const { datos, error } = useDatos("/datos/operaciones.json");

  useEffect(() => {
    document.title = "Operaciones | Manuel Lucero";
  }, []);

  return (
    <main id="contenido" className="pagina-dashboard">
      <div className="contenedor">
        <Link className="volver" to="/#proyectos">
          Volver a proyectos
        </Link>
        <p className="estado">Demostración</p>
        <h1>Análisis de indicadores operativos</h1>
        <p className="contexto">
          Una empresa quiere comparar el rendimiento de sus áreas semana a semana. Cada registro
          trae una meta y un resultado. El ejercicio usa datos ficticios.
        </p>
        <p className="tecnologias-linea">Python · SQL · Power BI · Excel</p>

        <EstadoDatos datos={datos} error={error}>
          {(info) => (
            <>
              <p className="advertencia">{info.advertencia}</p>

              <div className="kpi-grid">
                <KpiCard titulo="Actividades" valor={formatoNumero(info.kpis.actividades)} />
                <KpiCard
                  titulo="Cumplimiento promedio"
                  valor={formatoPorcentaje(info.kpis.cumplimiento_promedio)}
                  detalle="Media de resultado / meta"
                />
                <KpiCard
                  titulo="Actividades cumplidas"
                  valor={formatoNumero(info.kpis.actividades_cumplidas)}
                  detalle={formatoPorcentaje(info.kpis.porcentaje_cumplidas)}
                />
                <KpiCard titulo="Horas trabajadas" valor={formatoNumero(info.kpis.horas_trabajadas)} />
              </div>

              <div className="graficos">
                <Grafico
                  titulo="Cumplimiento por área"
                  nota="En cada área el cumplimiento es la suma de resultados dividida por la suma de metas."
                >
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={info.por_area}>
                      <CartesianGrid stroke="#334155" strokeDasharray="3 3" />
                      <XAxis dataKey="area" tick={estiloEje} interval={0} angle={-28} textAnchor="end" height={72} />
                      <YAxis tick={estiloEje} domain={[0, 100]} unit="%" width={48} />
                      <Tooltip contentStyle={estiloTooltip} formatter={(valor) => formatoPorcentaje(valor)} />
                      <Bar dataKey="cumplimiento" name="Cumplimiento" fill="#3B82F6" radius={[4, 4, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </Grafico>

                <Grafico titulo="Estado de las actividades">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie data={info.por_estado} dataKey="actividades" nameKey="estado" outerRadius={95} stroke="#0B1120">
                        {info.por_estado.map((estado) => (
                          <Cell key={estado.estado} fill={colorEstado[estado.estado] || "#94A3B8"} />
                        ))}
                      </Pie>
                      <Tooltip contentStyle={estiloTooltip} formatter={formatoNumero} />
                      <Legend wrapperStyle={estiloLeyenda} />
                    </PieChart>
                  </ResponsiveContainer>
                </Grafico>

                <Grafico
                  titulo="Tendencia semanal"
                  nota="El eje empieza en cero. La etiqueta de cada punto conserva el año y la semana ISO."
                  ancho
                >
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={info.evolucion_semanal}>
                      <CartesianGrid stroke="#334155" strokeDasharray="3 3" />
                      <XAxis dataKey="etiqueta" tick={estiloEje} interval={3} />
                      <YAxis tick={estiloEje} domain={[0, 100]} unit="%" width={48} />
                      <Tooltip
                        contentStyle={estiloTooltip}
                        formatter={(valor) => formatoPorcentaje(valor)}
                        labelFormatter={(_, items) => items?.[0]?.payload?.clave || ""}
                      />
                      <Line
                        type="monotone"
                        dataKey="cumplimiento"
                        name="Cumplimiento promedio"
                        stroke="#22D3EE"
                        strokeWidth={2}
                        dot={false}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </Grafico>

                <Grafico
                  titulo="Comparación mensual"
                  nota="Diciembre tiene menos registros: el archivo llega hasta el 17 de diciembre, cuando se completan las 1.500 filas."
                  ancho
                >
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={info.comparacion_mensual}>
                      <CartesianGrid stroke="#334155" strokeDasharray="3 3" />
                      <XAxis dataKey="etiqueta" tick={estiloEje} />
                      <YAxis tick={estiloEje} domain={[0, 100]} unit="%" width={48} />
                      <Tooltip contentStyle={estiloTooltip} formatter={(valor) => formatoPorcentaje(valor)} />
                      <Bar dataKey="cumplimiento" name="Cumplimiento promedio" fill="#3B82F6" radius={[4, 4, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </Grafico>
              </div>

              <h2>Indicadores por área</h2>
              <p className="nota">{info.nota_productividad}</p>
              <Tabla columnas={columnasArea} filas={info.por_area} clave="area" />

              <h2>Comparación entre meses</h2>
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
