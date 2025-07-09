import { notFound, redirect } from "next/navigation";
import { deleteProduct, updateProduct } from "./actions";
import { graphql } from "@/__generated__";
import {
  AdminProductDetailFragment,
  AdminProductOldVersionFragment,
} from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { Column, DataTable } from "@/components/DataTable";
import SignInRequired from "@/components/errors/SignInRequired";
import FormattedDateTime from "@/components/FormattedDateTime";
import { Field } from "@/components/forms/models";
import { SchemaForm } from "@/components/forms/SchemaForm";
import SubmitButton from "@/components/forms/SubmitButton";
import ModalButton from "@/components/ModalButton";
import TicketAdminTabs from "@/components/tickets/admin/TicketAdminTabs";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading, {
  ViewHeadingActions,
  ViewHeadingActionsWrapper,
} from "@/components/ViewHeading";
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
    canDelete

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
    return void redirect(`/${eventSlug}/products/${product.supersededBy.id}`);
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
    return void redirect(`/${eventSlug}/products/${product.supersededBy.id}`);
  }

  const selectedQuotas = product.quotas.map((quota) => "" + quota.id);

  const baseFields: Field[] = [
    {
      slug: "title",
      title: t.clientAttributes.title,
      type: "SingleLineText",
    },
    {
      slug: "description",
      type: "MultiLineText",
      rows: 3,
      ...t.clientAttributes.description,
    },
    {
      slug: "price",
      type: "DecimalField",
      decimalPlaces: 2,
      ...t.clientAttributes.unitPrice,
    },
    {
      slug: "eticketsPerProduct",
      type: "NumberField",
      ...t.clientAttributes.eticketsPerProduct,
    },
    {
      slug: "maxPerOrder",
      type: "NumberField",
      ...t.clientAttributes.maxPerOrder,
    },
  ];

  const fields: Field[] = baseFields.concat([
    {
      slug: "quotas",
      type: "MultiSelect",
      choices: quotas.map((quota) => ({
        slug: "" + quota.id,
        title: `${quota.name} (${quota.countTotal} ${t.clientAttributes.quantity.unit})`,
      })),
      ...t.clientAttributes.quotas,
    },
    {
      slug: "scheduleHeading",
      title: t.clientAttributes.isAvailable,
      type: "StaticText",
    },
    {
      slug: "availableFrom",
      type: "DateTimeField",
      ...t.clientAttributes.availableFrom,
    },
    {
      slug: "availableUntil",
      type: "DateTimeField",
      ...t.clientAttributes.availableUntil,
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
      title: t.clientAttributes.createdAt,
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
                {t.clientAttributes.revisions.current}
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
      title: t.clientAttributes.title,
      className: "col-4 align-middle",
    },
    {
      slug: "price",
      title: t.clientAttributes.unitPrice.title,
      getCellContents: (product) => formatMoney(product.price),
      className: "col-1 align-middle",
    },
  ];

  return (
    <ViewContainer>
      <ViewHeadingActionsWrapper>
        <ViewHeading>
          {translations.Tickets.admin.title}
          <ViewHeading.Sub>{t.forEvent(event.name)}</ViewHeading.Sub>
        </ViewHeading>
        <ViewHeadingActions>
          <ModalButton
            title={t.actions.deleteProduct.title}
            messages={t.actions.deleteProduct.modalActions}
            action={
              product.canDelete
                ? deleteProduct.bind(null, locale, eventSlug, productId)
                : undefined
            }
            className="btn btn-outline-danger"
          >
            {product.canDelete
              ? t.actions.deleteProduct.confirmation(product.title)
              : t.actions.deleteProduct.cannotDelete}
          </ModalButton>
        </ViewHeadingActions>
      </ViewHeadingActionsWrapper>

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
          <h5 className="card-title">{t.clientAttributes.revisions.title}</h5>
          <p className="card-text">
            {t.clientAttributes.revisions.description}
          </p>
          <DataTable columns={revisionsColumns} rows={revisions} />
        </div>
      </div>
    </ViewContainer>
  );
}
