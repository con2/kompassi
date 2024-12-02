export default function formatMoney(value: string) {
  return parseFloat(value).toFixed(2).replace(".", ",") + " €";
}
