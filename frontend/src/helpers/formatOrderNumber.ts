function formatOrderNumber(orderNumber: number) {
  return `#${orderNumber.toString().padStart(6, "0")}`;
}
