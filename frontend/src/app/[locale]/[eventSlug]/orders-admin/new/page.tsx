import Link from "next/link";
import { notFound } from "next/navigation";

import Alert from "react-bootstrap/Alert";
import Card from "react-bootstrap/Card";
import CardBody from "react-bootstrap/CardBody";
import { getAvailabilityMessage } from "../../products/page";
import ProductsForm from "../../tickets/ProductsForm";
import { adminCreateOrder } from "./actions";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import SignInRequired from "@/components/errors/SignInRequired";
import { Field } from "@/components/forms/models";
import { SchemaForm } from "@/components/forms/SchemaForm";
import SubmitButton from "@/components/forms/SubmitButton";
import ContactForm from "@/components/tickets/ContactForm";
import ProductCard from "@/components/tickets/ProductCard";
import TicketsAdminView from "@/components/tickets/TicketsAdminView";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

graphql(`
  fragment NewOrderProduct on FullProductType {
    id
    title
    description
    price
    isAvailable
    availableFrom
    availableUntil
    countPaid
    countReserved
    countAvailable
    maxPerOrder
  }
`);

const query = graphql(`
  query NewOrderPage($eventSlug: String!) {
    event(slug: $eventSlug) {
      name
      slug

      tickets {
        products {
          ...NewOrderProduct
        }
      }
    }
  }
`);

interface Props {
  params: {
    locale: string;
    eventSlug: string;
  };
  searchParams: Record<string, string>;
}

export async function generateMetadata({ params }: Props) {
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Tickets.Order;

  // TODO encap
  const session = await auth();
  if (!session) {
    return translations.SignInRequired.metadata;
  }

  const { data } = await getClient().query({
    query,
    variables: { eventSlug },
  });

  if (!data.event?.tickets) {
    notFound();
  }

  const title = getPageTitle({
    event: data.event,
    viewTitle: t.actions.newOrder.label,
    translations,
  });

  return {
    title,
  };
}

export const revalidate = 0;

export default async function OrdersPage({ params, searchParams }: Props) {
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Tickets.Order;
  const producT = translations.Tickets.Product;

  // TODO encap
  const session = await auth();
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  const { data } = await getClient().query({
    query,
    variables: { eventSlug },
  });

  if (!data.event?.tickets) {
    notFound();
  }

  const event = data.event;
  const products = data.event.tickets.products.map((product) => ({
    ...product,
    // The admin may purchase a product if there is stock, despite availability.
    available: product.countAvailable ? product.countAvailable > 0 : false,
    // The admin is not limited by maxPerOrder.
    maxPerOrder: product.countAvailable ?? 0,
  }));

  const fields: Field[] = [
    {
      slug: "language",
      type: "SingleSelect",
      presentation: "dropdown",
      required: true,
      ...t.attributes.language,
      choices: Object.entries(
        translations.LanguageSwitcher.supportedLanguages,
      ).map(([slug, title]) => ({
        slug,
        title,
      })),
    },
  ];

  function ProductsLink({ children }: { children: React.ReactNode }) {
    return (
      <Link href={`/${event.slug}/products`} className="link-subtle">
        {children}
      </Link>
    );
  }

  return (
    <TicketsAdminView
      translations={translations}
      event={event}
      searchParams={searchParams}
      active="orders"
    >
      <Alert variant="warning" className="mt-4">
        <h4>{t.actions.newOrder.title}</h4>
        <CardBody>{t.actions.newOrder.message}</CardBody>
      </Alert>

      <h4 className="mt-4">{t.attributes.products}</h4>
      {products.length === 0 && (
        <Alert variant="danger">
          {t.actions.newOrder.errors.noProducts(ProductsLink)}
        </Alert>
      )}
      <ProductsForm
        messages={t.errors}
        onSubmit={adminCreateOrder.bind(null, locale, eventSlug)}
      >
        {products.map((product) => (
          <ProductCard key={product.id} product={product} messages={producT}>
            <div className="form-text">
              <span className="me-3">
                {producT.clientAttributes.countReserved.title}:{" "}
                {product.countReserved}
              </span>{" "}
              <span className="me-3">
                {producT.clientAttributes.countPaid}: {product.countPaid}
              </span>
              <span className="me-3">
                {producT.clientAttributes.countAvailable}:{" "}
                {product.countAvailable}
              </span>
              <span>{getAvailabilityMessage(product, producT, locale)}</span>
            </div>
          </ProductCard>
        ))}

        <h4 className="mt-4 mb-4">{t.contactForm.title}</h4>
        <Card className="mb-4">
          <CardBody>
            <ContactForm
              messages={translations}
              termsAndConditionsUrl={undefined}
              isAdmin={true}
            />
            <SchemaForm
              fields={fields}
              messages={translations.SchemaForm}
              values={{ language: locale }}
            />
          </CardBody>
        </Card>

        <div className="d-grid gap-2 mb-4">
          <SubmitButton className="btn btn-primary btn-lg">
            {t.actions.newOrder.actions.submit}
          </SubmitButton>
        </div>
      </ProductsForm>
    </TicketsAdminView>
  );
}
