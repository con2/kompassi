import Link from "next/link";
import { ReactNode } from "react";
import OpenInNewTab from "./google-material-symbols/OpenInNewTab";

export interface Tab {
  slug: string;
  href?: string;
  title: string;
  external?: boolean;
  getTabHeader?: () => ReactNode;
  disabled?: boolean;
}

interface Props {
  tabs: Tab[];
  active: string;
}

/// Tabs as a server component. You need to add the tabs to each page that uses it.
export default function ServerTabs({ tabs, active }: Props) {
  function defaultGetTabHeader(this: Tab) {
    const classes = ["nav-link"];

    if (this.slug === active) {
      classes.push("active");
    }

    if (this.disabled) {
      classes.push("disabled");
    }

    if (this.external) {
      return (
        <a
          className="nav-link"
          href={this.href}
          target="_blank"
          rel="noopener noreferrer"
        >
          {this.title} <OpenInNewTab />
        </a>
      );
    }

    return (
      <Link className={classes.join(" ")} href={this.href || ""}>
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
