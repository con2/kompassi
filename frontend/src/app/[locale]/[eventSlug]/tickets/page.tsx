import Card from "react-bootstrap/Card";
import CardBody from "react-bootstrap/CardBody";
import { createOrder } from "./actions";
import ProductsForm from "./ProductsForm";
import SubmitButton from "@/components/forms/SubmitButton";
import ContactForm from "@/components/tickets/ContactForm";
import ProductCard from "@/components/tickets/ProductCard";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
import getPageTitle from "@/helpers/getPageTitle";
import { getProducts } from "@/services/tickets";
import { getTranslations } from "@/translations";

interface Props {
  params: Promise<{
    locale: string;
    eventSlug: string;
  }>;
}

export async function generateMetadata(props: Props) {
  const params = await props.params;
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

export default async function TicketsPage(props: Props) {
  const params = await props.params;
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
          <ViewHeading.Sub>{tickeT.forEvent(event.name)}</ViewHeading.Sub>
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
        messages={{ NO_PRODUCTS_SELECTED: t.errors.NO_PRODUCTS_SELECTED }}
      >
        {products.map((product) => {
          return (
            <ProductCard
              key={product.id}
              product={product}
              messages={producT}
            />
          );
        })}

        <h2 className="mt-4 mb-4">{t.contactForm.title}</h2>
        <Card className="mb-3">
          <CardBody>
            <ContactForm
              messages={translations}
              termsAndConditionsUrl={event.termsAndConditionsUrl}
            />
          </CardBody>
        </Card>

        <div className="d-grid gap-2 mb-4">
          <SubmitButton className="btn btn-primary btn-lg">
            {t.actions.purchase}
          </SubmitButton>
        </div>
      </ProductsForm>
    </ViewContainer>
  );
}
