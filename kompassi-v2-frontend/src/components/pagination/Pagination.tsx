import Link from "next/link";
import type { ReactNode } from "react";

import type { Translations } from "@/translations/en";

export interface PaginationInfo {
  page: number;
  totalPages: number;
  totalCount: number;
  hasPrevious: boolean;
  hasNext: boolean;
}

interface Props {
  pagination: PaginationInfo;
  /// The current search params. The page links preserve every other param.
  searchParams: Record<string, string>;
  messages: Translations["Pagination"];
  className?: string;
}

/// Reads the requested page from the search params. Page numbers start from 1.
/// Anything that is not a positive integer means the first page.
export function getPage(searchParams: Record<string, string>): number {
  const page = parseInt(searchParams.page ?? "", 10);
  return Number.isInteger(page) && page >= 1 ? page : 1;
}

function pageHref(searchParams: Record<string, string>, page: number) {
  const params = new URLSearchParams(searchParams);
  if (page <= 1) {
    params.delete("page");
  } else {
    params.set("page", String(page));
  }
  const queryString = params.toString();
  return queryString ? `?${queryString}` : "?";
}

interface PageLinkProps {
  page: number;
  enabled: boolean;
  searchParams: Record<string, string>;
  label: string;
  children: ReactNode;
}

function PageLink({
  page,
  enabled,
  searchParams,
  label,
  children,
}: PageLinkProps) {
  return (
    <li className={`page-item ${enabled ? "" : "disabled"}`}>
      {enabled ? (
        <Link
          className="page-link"
          href={pageHref(searchParams, page)}
          aria-label={label}
          title={label}
        >
          {children}
        </Link>
      ) : (
        <span className="page-link" aria-disabled="true">
          {children}
        </span>
      )}
    </li>
  );
}

/// Page navigation for server components that paginate via the `page` search param.
/// Renders nothing when everything fits on one page.
export default function Pagination({
  pagination,
  searchParams,
  messages,
  className = "",
}: Props) {
  const { page, totalPages, hasPrevious, hasNext } = pagination;

  if (totalPages <= 1) {
    return null;
  }

  return (
    <nav aria-label={messages.title} className={className}>
      <ul className="pagination pagination-sm mb-0">
        <PageLink
          page={1}
          enabled={hasPrevious}
          searchParams={searchParams}
          label={messages.first}
        >
          «
        </PageLink>
        <PageLink
          page={page - 1}
          enabled={hasPrevious}
          searchParams={searchParams}
          label={messages.previous}
        >
          ‹
        </PageLink>
        <li className="page-item disabled">
          <span className="page-link text-body">
            {messages.pageOf(page, totalPages)}
          </span>
        </li>
        <PageLink
          page={page + 1}
          enabled={hasNext}
          searchParams={searchParams}
          label={messages.next}
        >
          ›
        </PageLink>
        <PageLink
          page={totalPages}
          enabled={hasNext}
          searchParams={searchParams}
          label={messages.last}
        >
          »
        </PageLink>
      </ul>
    </nav>
  );
}
