import Link from "next/link";

export interface Tab {
  slug: string;
  href?: string;
  title: string;
}

interface Props {
  tabs: Tab[];
  active: string;
}

/// Tabs as a server component. You need to add the tabs to each page that uses it.
export default function Tabs({ tabs, active }: Props) {
  return (
    <ul className="nav nav-tabs">
      {tabs.map(({ slug, href, title }) => (
        <li key={slug} className="nav-item">
          <Link
            className={`nav-link ${slug === active ? "active" : ""}`}
            href={href || ""}
          >
            {title}
          </Link>
        </li>
      ))}
    </ul>
  );
}
