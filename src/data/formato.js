export const colores = [
  "#3B82F6",
  "#22D3EE",
  "#38BDF8",
  "#818CF8",
  "#2DD4BF",
  "#60A5FA",
  "#67E8F9",
  "#93C5FD",
];

export const estiloLeyenda = {
  color: "#94A3B8",
};

export const estiloTooltip = {
  background: "#1E293B",
  border: "1px solid #334155",
  borderRadius: 8,
  color: "#F8FAFC",
};

export const estiloEje = {
  stroke: "#94A3B8",
  fontSize: 12,
};

export function formatoNumero(valor) {
  return new Intl.NumberFormat("es-CO", { maximumFractionDigits: 0 }).format(valor);
}

export function formatoPorcentaje(valor) {
  return `${new Intl.NumberFormat("es-CO", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(valor)} %`;
}

export function formatoMoneda(valor) {
  return new Intl.NumberFormat("es-CO", {
    style: "currency",
    currency: "COP",
    maximumFractionDigits: 0,
  }).format(valor);
}

export function formatoDecimal(valor) {
  return new Intl.NumberFormat("es-CO", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(valor);
}
