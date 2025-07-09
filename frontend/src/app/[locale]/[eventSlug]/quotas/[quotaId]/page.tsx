import Link from "next/link";
import { notFound } from "next/navigation";
import { deleteQuota, updateQuota } from "./actions";
import { graphql } from "@/__generated__";
import { QuotaProductFragment } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { Column, DataTable } from "@/components/DataTable";
import SignInRequired from "@/components/errors/SignInRequired";
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
import { getTranslations } from "@/translations";

graphql(`
  fragment QuotaProduct on LimitedProductType {
    id
    title
    price
    countReserved
  }
`);

const query = graphql(`
  query AdminQuotaDetailPage($eventSlug: String!, $quotaId: Int!) {
    event(slug: $eventSlug) {
      name
      slug

      tickets {
        quota(id: $quotaId) {
          id
          name
          countReserved
          quota: countTotal
          canDelete

          products {
            ...QuotaProduct
          }
        }
      }
    }
  }
`);

interface Props {
  params: {
    locale: string;
    eventSlug: string;
    quotaId: string;
  };
}

export const revalidate = 0;

export default async function AdminQuotaDetailPage({ params }: Props) {
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Tickets.Quota;
  const producT = translations.Tickets.Product;
  const session = await auth();

  const quotaId = parseInt(params.quotaId, 10);

  // TODO encap
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, quotaId },
  });

  if (!data.event?.tickets?.quota) {
    notFound();
  }

  const event = data.event;
  const quota = data.event.tickets.quota;
  const products = data.event.tickets.quota.products;

  const fields: Field[] = [
    {
      slug: "name",
      title: t.attributes.name,
      type: "SingleLineText",
    },
    {
      slug: "quota",
      type: "NumberField",
      title: t.attributes.countTotal.title,
      minValue: quota.countReserved,
      helpText: t.attributes.countTotal.helpText(quota.countReserved),
    },
  ];

  const productColumns: Column<QuotaProductFragment>[] = [
    {
      slug: "title",
      title: producT.clientAttributes.title,
      className: "col-4 align-middle",
      getCellContents: (product) => (
        <Link
          href={`/${event.slug}/products/${product.id}`}
          className="link-subtle"
        >
          {product.title}
        </Link>
      ),
    },
    {
      slug: "price",
      title: producT.clientAttributes.unitPrice.title,
      getCellContents: (product) => formatMoney(product.price),
      className: "col-1 align-middle",
    },
    {
      slug: "countReserved",
      title: producT.clientAttributes.countReserved.title,
      className: "text-end align-middle col-1",
    },
  ];

  const totalSold = products.reduce(
    (acc, product) => acc + product.countReserved,
    0,
  );

  return (
    <ViewContainer>
      <ViewHeadingActionsWrapper>
        <ViewHeading>
          {translations.Tickets.admin.title}
          <ViewHeading.Sub>{t.forEvent(event.name)}</ViewHeading.Sub>
        </ViewHeading>
        <ViewHeadingActions>
          <ModalButton
            title={t.actions.deleteQuota.title}
            messages={t.actions.deleteQuota.modalActions}
            action={
              quota.canDelete
                ? deleteQuota.bind(null, locale, eventSlug, params.quotaId)
                : undefined
            }
            className="btn btn-outline-danger"
          >
            {quota.canDelete
              ? t.actions.deleteQuota.confirmation(quota.name)
              : t.actions.deleteQuota.cannotDelete}
          </ModalButton>
        </ViewHeadingActions>
      </ViewHeadingActionsWrapper>

      <TicketAdminTabs
        eventSlug={eventSlug}
        active="quotas"
        translations={translations}
      />

      <div className="card mb-4">
        <div className="card-body">
          <h5 className="card-title">{t.actions.editQuota}</h5>
          <form action={updateQuota.bind(null, locale, eventSlug, quota.id)}>
            <SchemaForm
              fields={fields}
              values={quota}
              messages={translations.SchemaForm}
              headingLevel="h5"
            />
            <SubmitButton>{t.actions.saveQuota}</SubmitButton>
          </form>
        </div>
      </div>

      <div className="card mb-4">
        <div className="card-body">
          <h5 className="card-title">{t.attributes.products.title}</h5>
          <p className="card-text">{t.attributes.products.helpText}</p>
          <DataTable columns={productColumns} rows={products}>
            <tfoot>
              <tr>
                <th scope="row" colSpan={2}>
                  {t.attributes.totalReserved}
                </th>
                <td className="text-end align-middle">{totalSold}</td>
              </tr>
            </tfoot>
          </DataTable>
        </div>
      </div>
    </ViewContainer>
  );
}
