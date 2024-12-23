import { notFound, redirect } from "next/navigation";
import { updateProduct } from "./actions";
import { graphql } from "@/__generated__";
import {
  AdminProductDetailFragment,
  AdminProductOldVersionFragment,
} from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { Column, DataTable } from "@/components/DataTable";
import FormattedDateTime from "@/components/FormattedDateTime";
import { Field } from "@/components/forms/models";
import { SchemaForm } from "@/components/forms/SchemaForm";
import SubmitButton from "@/components/forms/SubmitButton";
import ModalButton from "@/components/ModalButton";
import SignInRequired from "@/components/SignInRequired";
import TicketAdminTabs from "@/components/tickets/admin/TicketAdminTabs";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
import formatMoney from "@/helpers/formatMoney";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

graphql(`
  fragment AdminProductOldVersion on LimitedProductType {
    createdAt
    title
    description
    price
    eticketsPerProduct
    maxPerOrder
  }
`);

graphql(`
  fragment AdminProductDetail on FullProductType {
    id
    createdAt
    title
    description
    price
    eticketsPerProduct
    maxPerOrder
    availableFrom
    availableUntil
    quotas {
      id
    }

    supersededBy {
      id
    }

    oldVersions {
      ...AdminProductOldVersion
    }
  }
`);

const query = graphql(`
  query AdminProductDetailPage($eventSlug: String!, $productId: String!) {
    event(slug: $eventSlug) {
      name
      slug

      tickets {
        quotas {
          id
          name
          countTotal
        }

        product(id: $productId) {
          ...AdminProductDetail
        }
      }
    }
  }
`);

type Revision =
  | (AdminProductOldVersionFragment & { isCurrent: false })
  | (AdminProductDetailFragment & { isCurrent: true });

interface Props {
  params: {
    locale: string;
    eventSlug: string;
    productId: string;
  };
}

export const revalidate = 0;

export async function generateMetadata({ params }: Props) {
  const { locale, eventSlug, productId } = params;
  const translations = getTranslations(locale);
  const t = translations.Tickets.Product;

  // TODO encap
  const session = await auth();
  if (!session) {
    return translations.SignInRequired.metadata;
  }

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, productId },
  });

  if (!data.event?.tickets?.product) {
    notFound();
  }

  const event = data.event;
  const product = data.event.tickets.product;

  if (product.supersededBy?.id) {
    return void redirect(
      `/${locale}/${eventSlug}/products/${product.supersededBy.id}`,
    );
  }

  const title = getPageTitle({
    event,
    viewTitle: t.listTitle,
    subject: product.title,
    translations,
  });

  return {
    title,
  };
}

export default async function AdminProductDetailPage({ params }: Props) {
  const { locale, eventSlug, productId } = params;
  const translations = getTranslations(locale);
  const t = translations.Tickets.Product;

  // TODO encap
  const session = await auth();
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, productId },
  });

  if (!data.event?.tickets?.product) {
    notFound();
  }

  const event = data.event;
  const product = data.event.tickets.product;
  const quotas = data.event.tickets.quotas;

  if (product.supersededBy?.id) {
    return void redirect(
      `/${locale}/${eventSlug}/products/${product.supersededBy.id}`,
    );
  }

  const selectedQuotas = product.quotas.map((quota) => "" + quota.id);

  const baseFields: Field[] = [
    {
      slug: "title",
      title: t.attributes.title,
      type: "SingleLineText",
    },
    {
      slug: "description",
      type: "MultiLineText",
      rows: 3,
      ...t.attributes.description,
    },
    {
      slug: "price",
      type: "DecimalField",
      decimalPlaces: 2,
      ...t.attributes.unitPrice,
    },
    {
      slug: "eticketsPerProduct",
      type: "NumberField",
      ...t.attributes.eticketsPerProduct,
    },
    {
      slug: "maxPerOrder",
      type: "NumberField",
      ...t.attributes.maxPerOrder,
    },
  ];

  const fields: Field[] = baseFields.concat([
    {
      slug: "quotas",
      type: "MultiSelect",
      choices: quotas.map((quota) => ({
        slug: "" + quota.id,
        title: `${quota.name} (${quota.countTotal} ${t.attributes.quantity.unit})`,
      })),
      ...t.attributes.quotas,
    },
    {
      slug: "scheduleHeading",
      title: t.attributes.isAvailable.title,
      type: "StaticText",
    },
    {
      slug: "availableFrom",
      type: "DateTimeField",
      ...t.attributes.availableFrom,
    },
    {
      slug: "availableUntil",
      type: "DateTimeField",
      ...t.attributes.availableUntil,
    },
  ]);

  const values = {
    ...product,
    quotas: selectedQuotas,
  };

  const revisions: Revision[] = [
    { ...product, isCurrent: true },
    ...product.oldVersions.map(
      (oldVersion) =>
        ({
          ...oldVersion,
          isCurrent: false,
        }) as const,
    ),
  ];

  const revisionsColumns: Column<Revision>[] = [
    {
      slug: "createdAt",
      title: t.attributes.createdAt,
      className: "col-2 align-middle",
      getCellContents: (product) => (
        <>
          {product.isCurrent ? (
            <>
              <FormattedDateTime
                value={product.createdAt}
                locale={locale}
                scope={event}
                session={session}
              />
              <span className="badge bg-primary ms-2">
                {t.attributes.revisions.current}
              </span>
            </>
          ) : (
            <ModalButton
              title={t.actions.viewOldVersion.title}
              label={
                <FormattedDateTime
                  value={product.createdAt}
                  locale={locale}
                  scope={event}
                  session={session}
                />
              }
              labelTitle={t.actions.viewOldVersion.label}
              messages={t.actions.viewOldVersion.modalActions}
            >
              <SchemaForm
                fields={baseFields}
                values={product}
                messages={translations.SchemaForm}
                readOnly
              />
            </ModalButton>
          )}
        </>
      ),
    },
    {
      slug: "title",
      title: t.attributes.title,
      className: "col-4 align-middle",
    },
    {
      slug: "price",
      title: t.attributes.unitPrice.title,
      getCellContents: (product) => formatMoney(product.price),
      className: "col-1 align-middle",
    },
  ];

  return (
    <ViewContainer>
      <ViewHeading>
        {translations.Tickets.admin.title}
        <ViewHeading.Sub>{t.forEvent(event.name)}</ViewHeading.Sub>
      </ViewHeading>

      <TicketAdminTabs
        eventSlug={eventSlug}
        active="products"
        translations={translations}
      />

      <div className="card mb-4">
        <div className="card-body">
          <h5 className="card-title">{t.actions.editProduct}</h5>
          <form
            action={updateProduct.bind(null, locale, eventSlug, product.id)}
          >
            <SchemaForm
              fields={fields}
              values={values}
              messages={translations.SchemaForm}
              headingLevel="h5"
            />
            <SubmitButton>{t.actions.saveProduct}</SubmitButton>
          </form>
        </div>
      </div>

      <div className="card mb-4">
        <div className="card-body">
          <h5 className="card-title">{t.attributes.revisions.title}</h5>
          <p className="card-text">{t.attributes.revisions.description}</p>
          <DataTable columns={revisionsColumns} rows={revisions} />
        </div>
      </div>
    </ViewContainer>
  );
}
