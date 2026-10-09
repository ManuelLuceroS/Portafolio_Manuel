export default function Grafico({ titulo, nota, alto, ancho, children }) {
  const clase = ancho ? "grafico grafico-ancho" : "grafico";
  const lienzo = alto ? "grafico-lienzo alto" : "grafico-lienzo";

  return (
    <section className={clase}>
      <h3>{titulo}</h3>
      {nota ? <p className="nota-grafico">{nota}</p> : null}
      <div className={lienzo}>{children}</div>
    </section>
  );
}
