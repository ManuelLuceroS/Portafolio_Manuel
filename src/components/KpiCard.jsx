export default function KpiCard({ titulo, valor, detalle }) {
  return (
    <article className="kpi">
      <p className="kpi-titulo">{titulo}</p>
      <p className="kpi-valor">{valor}</p>
      {detalle ? <p className="kpi-detalle">{detalle}</p> : null}
    </article>
  );
}
