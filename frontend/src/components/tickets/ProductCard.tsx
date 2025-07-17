import { ReactNode } from "react";
import Card from "react-bootstrap/Card";
import CardBody from "react-bootstrap/CardBody";
import CardTitle from "react-bootstrap/CardTitle";
import formatMoney from "@/helpers/formatMoney";
import { Product } from "@/services/tickets";
import { Translations } from "@/translations/en";

interface Props {
  product: Product;
  messages: Translations["Tickets"]["Product"];
  children?: ReactNode;
}

export default function ProductCard({ product, messages: t, children }: Props) {
  const className = product.available ? "" : "text-muted";
  return (
    <Card key={product.id} className="mb-3">
      <CardBody className={`row ${className}`}>
        <div className="col-md-8 m-md-0 mb-2">
          <CardTitle>{product.title}</CardTitle>
          {product.description}
          {children}
        </div>

        <div className={`col-md m-md-0 mb-3 fs-4 text-md-end`}>
          {formatMoney(product.price)}
        </div>

        <div className={`col-md fs-4`}>
          <label htmlFor={`quantity-${product.id}`} className="visually-hidden">
            {t.clientAttributes.quantity.quantityForProduct} {product.title}
          </label>
          {product.available ? (
            <input
              type="number"
              className="form-control"
              id={`quantity-${product.id}`}
              name={`quantity-${product.id}`}
              min={0}
              defaultValue=""
              max={product.maxPerOrder}
              placeholder={t.clientAttributes.quantity.placeholder + "…"}
            />
          ) : (
            t.clientAttributes.soldOut
          )}
        </div>
      </CardBody>
    </Card>
  );
}
