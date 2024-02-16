import Link from "next/link";
import { ReactNode } from "react";

export interface Tab {
  slug: string;
  href?: string;
  title: string;
  getTabHeader?: () => ReactNode;
}

interface Props {
  tabs: Tab[];
  active: string;
}

/// Tabs as a server component. You need to add the tabs to each page that uses it.
export default function ServerTabs({ tabs, active }: Props) {
  function defaultGetTabHeader(this: Tab) {
    return (
      <Link
        className={`nav-link ${this.slug === active ? "active" : ""}`}
        href={this.href || ""}
      >
        {this.title}
      </Link>
    );
  }

  return (
    <ul className="nav nav-tabs">
      {tabs.map((tab) => (
        <li key={tab.slug} className="nav-item">
          {tab.getTabHeader?.call(tab) || defaultGetTabHeader.call(tab)}
        </li>
      ))}
    </ul>
  );
}
