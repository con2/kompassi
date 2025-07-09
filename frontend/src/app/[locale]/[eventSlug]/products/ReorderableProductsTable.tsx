"use client";

import Link from "next/link";
import { useCallback, useState } from "react";

import { PreparedProduct } from "./page";
import { Column } from "@/components/DataTable";
import { ReorderableDataTable } from "@/components/ReorderableDataTable";
import formatMoney from "@/helpers/formatMoney";
import type { Translations } from "@/translations/en";

interface Props {
  event: {
    slug: string;
  };
  products: PreparedProduct[];
  messages: Translations["Tickets"]["Product"]["clientAttributes"];
  onReorder: (productIds: string[]) => void;
}

export default function ReorderableProductsTable({
  event,
  products,
  messages: t,
  onReorder,
}: Props) {
  const [rows, setRows] = useState(Array.from(products));

  const handleReorder = useCallback(
    (rows: PreparedProduct[]) => {
      setRows(rows);
      onReorder(rows.map((product) => product.id));
    },
    [onReorder],
  );

  const columns: Column<PreparedProduct>[] = [
    {
      slug: "title",
      title: t.product,
      getCellContents: (product) => (
        <Link
          className="link-subtle"
          href={`/${event.slug}/products/${product.id}`}
        >
          {product.title}
        </Link>
      ),
    },
    {
      slug: "availabilityMessage",
      title: t.isAvailable,
    },
    {
      slug: "countPaid",
      title: t.countPaid,
      className: "text-end align-middle col-1",
    },
    {
      slug: "countReserved",
      title: t.countReserved.title,
      getHeaderContents: () => (
        <abbr title={t.countReserved.description}>{t.countReserved.title}</abbr>
      ),
      className: "text-end align-middle col-1",
    },
    {
      slug: "countAvailable",
      title: t.countAvailable,
      className: "text-end align-middle col-1",
    },
    {
      slug: "price",
      title: t.unitPrice.title,
      getCellContents: (product) => formatMoney(product.price),
      className: "text-end align-middle col-2",
    },
  ];

  // TODO let the backend calculate these with decimals
  const totalReserved = formatMoney(
    "" +
      products.reduce(
        (acc, product) =>
          acc + product.countReserved * parseFloat(product.price),
        0,
      ),
  );
  const totalPaid = formatMoney(
    "" +
      products.reduce(
        (acc, product) => acc + product.countPaid * parseFloat(product.price),
        0,
      ),
  );

  return (
    <ReorderableDataTable
      rows={rows}
      columns={columns}
      keyColumn="id"
      onReorderRows={handleReorder}
      messages={t}
    >
      <tfoot>
        <tr>
          <th
            colSpan={columns.length}
            className="text-end align-middle"
            scope="row"
          >
            {t.totalPaid}
          </th>
          <th className="text-end align-middle col-2">{totalPaid}</th>
        </tr>
        <tr>
          <th
            colSpan={columns.length}
            className="text-end align-middle"
            scope="row"
          >
            <abbr title={t.countReserved.description}>{t.totalReserved}</abbr>
          </th>
          <th className="text-end align-middle col-2">{totalReserved}</th>
        </tr>
      </tfoot>
    </ReorderableDataTable>
  );
}
