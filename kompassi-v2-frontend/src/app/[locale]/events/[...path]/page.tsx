import { redirect } from "next/navigation";

interface Props {
  params: Promise<{
    locale: string;
    path: string[];
  }>;
  searchParams: Promise<Record<string, string>>;
}

export default async function EventsRedirectPage(props: Props): Promise<never> {
  const searchParams = await props.searchParams;
  const params = await props.params;
  const { path } = params;
  const query = new URLSearchParams(searchParams).toString();
  return redirect(`/${path.join("/")}${query ? `?${query}` : ""}`);
}

export const generateMetadata = EventsRedirectPage;
