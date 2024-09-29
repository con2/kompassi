import { redirect } from "next/navigation";

interface Props {
  params: {
    locale: string;
    path: string[];
  };
  searchParams: Record<string, string>;
}

export function generateMetadata({ params, searchParams }: Props): never {
  const { path } = params;
  const query = new URLSearchParams(searchParams).toString();
  return redirect(`/${path.join("/")}${query ? `?${query}` : ""}`);
}

export default function EventsRedirectPage(props: Props): never {
  return generateMetadata(props);
}
