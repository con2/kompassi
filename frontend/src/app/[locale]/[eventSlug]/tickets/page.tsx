import { createOrder } from "./actions";
import ProductsForm from "./ProductsForm";
import ContactForm from "@/components/tickets/ContactForm";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
import formatMoney from "@/helpers/formatMoney";
import getPageTitle from "@/helpers/getPageTitle";
import { getProducts } from "@/services/tickets";
import { getTranslations } from "@/translations";

interface Props {
  params: {
    locale: string;
    eventSlug: string;
  };
}

export async function generateMetadata({ params }: Props) {
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Tickets;
  const { event } = await getProducts(locale, eventSlug);

  const title = getPageTitle({ translations, event, viewTitle: t.title });

  return {
    title,
  };
}

export const revalidate = 0;

export default async function TicketsPage({ params }: Props) {
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Tickets.Order;
  const producT = translations.Tickets.Product;
  const tickeT = translations.Tickets;
  const { event, products } = await getProducts(locale, eventSlug);

  if (
    products.length === 0 ||
    products.every((product) => !product.available)
  ) {
    return (
      <ViewContainer>
        <ViewHeading>
          {producT.noProducts.title}
          <ViewHeading.Sub>{producT.forEvent(event.name)}</ViewHeading.Sub>
        </ViewHeading>
        <p>{producT.noProducts.message}</p>
      </ViewContainer>
    );
  }

  return (
    <ViewContainer>
      <ViewHeading>
        {tickeT.title}
        <ViewHeading.Sub>{tickeT.forEvent(event.name)}</ViewHeading.Sub>
      </ViewHeading>

      <ProductsForm
        onSubmit={createOrder.bind(null, locale, eventSlug)}
        messages={{ noProductsSelectedError: t.errors.NO_PRODUCTS_SELECTED }}
      >
        <table className="table table-striped mt-4 mb-4">
          <thead>
            <tr className="row">
              <th className="col-8">{producT.clientAttributes.product}</th>
              <th className="col">
                {producT.clientAttributes.unitPrice.title}
              </th>
              <th className="col">{producT.clientAttributes.quantity.title}</th>
            </tr>
          </thead>
          <tbody>
            {products.map((product) => {
              const className = product.available ? "" : "text-muted";
              return (
                <tr key={product.id} className="row">
                  <td className={`col-8 ${className}`}>
                    <p>
                      <strong>{product.title}</strong>
                    </p>
                    {product.description}
                  </td>
                  <td className={`col fs-4 ${className}`}>
                    {formatMoney(product.price)}
                  </td>
                  <td className={`col fs-4 ${className}`}>
                    <label
                      htmlFor={`quantity-${product.id}`}
                      className="visually-hidden"
                    >
                      {producT.clientAttributes.quantity.title}
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
                      />
                    ) : (
                      producT.clientAttributes.soldOut
                    )}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>

        <h2 className="mb-4">{t.contactForm.title}</h2>
        <ContactForm
          messages={translations}
          termsAndConditionsUrl={event.termsAndConditionsUrl}
        />

        <div className="d-grid gap-2 mb-4">
          <button className="btn btn-primary btn-lg" type="submit">
            {t.actions.purchase}
          </button>
        </div>
      </ProductsForm>
    </ViewContainer>
  );
}
