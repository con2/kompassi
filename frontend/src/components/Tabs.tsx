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
