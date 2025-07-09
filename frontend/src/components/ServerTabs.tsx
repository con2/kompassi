import Link from "next/link";
import { ReactNode } from "react";

export interface Tab {
  slug: string;
  href?: string;
  title: string;
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
