import { createOrder } from "./actions";
import { getProducts } from "./service";
import { Field } from "@/components/forms/models";
import { SchemaForm } from "@/components/forms/SchemaForm";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
import formatMoney from "@/helpers/formatMoney";
import getPageTitle from "@/helpers/getPageTitle";
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
  const { event } = await getProducts(eventSlug);

  const title = getPageTitle({ translations, event, viewTitle: t.title });

  return {
    title,
  };
}

export const revalidate = 1;

export default async function TicketsPage({ params }: Props) {
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Tickets;
  const { event, products } = await getProducts(eventSlug);

  const fields: Field[] = [
    {
      slug: "firstName",
      type: "SingleLineText",
      required: true,
      ...t.contactForm.fields.firstName,
    },
    {
      slug: "lastName",
      type: "SingleLineText",
      required: true,
      ...t.contactForm.fields.lastName,
    },
    {
      slug: "email",
      type: "SingleLineText",
      required: true,
      ...t.contactForm.fields.email,
    },
    {
      slug: "phone",
      type: "SingleLineText",
      ...t.contactForm.fields.phone,
    },
  ];

  if (products.length === 0) {
    return (
      <ViewContainer>
        <ViewHeading>
          {t.noProducts.title}
          <ViewHeading.Sub>{t.forEvent(event.name)}</ViewHeading.Sub>
        </ViewHeading>
        <p>{t.noProducts.message}</p>
      </ViewContainer>
    );
  }

  return (
    <ViewContainer>
      <ViewHeading>
        {t.title}
        <ViewHeading.Sub>{t.forEvent(event.name)}</ViewHeading.Sub>
      </ViewHeading>

      <form action={createOrder.bind(null, locale, eventSlug)}>
        <table className="table table-striped mt-4 mb-5">
          <thead>
            <tr className="row">
              <th className="col-8">{t.productsTable.product}</th>
              <th className="col">{t.productsTable.unitPrice}</th>
              <th className="col">{t.productsTable.quantity.title}</th>
            </tr>
          </thead>
          <tbody>
            {products.map((product) => (
              <tr key={product.id} className="row">
                <td className="col-8">
                  <p>
                    <strong>{product.title}</strong>
                  </p>
                  {product.description}
                </td>
                <td className="col fs-4">{formatMoney(product.price)}</td>
                <td className="col">
                  <label
                    htmlFor={`quantity-${product.id}`}
                    className="visually-hidden"
                  >
                    {t.productsTable.quantity.title}
                  </label>
                  <input
                    type="number"
                    className="form-control"
                    id={`quantity-${product.id}`}
                    name={`quantity-${product.id}`}
                    defaultValue={0}
                  />
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        <div className="mb-5">
          <h2>{t.contactForm.title}</h2>
          <SchemaForm fields={fields} messages={translations.SchemaForm} />
        </div>

        <div className="d-grid gap-2 mb-4">
          <button className="btn btn-primary btn-lg" type="submit">
            {t.purchaseButtonText}
          </button>
        </div>
      </form>
    </ViewContainer>
  );
}
