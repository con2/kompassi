export interface Order {
  customer: {
    firstName: string;
    lastName: string;
    email: string;
    phone?: string;
  };
  products: {
    [productId: string]: number;
  };
}
