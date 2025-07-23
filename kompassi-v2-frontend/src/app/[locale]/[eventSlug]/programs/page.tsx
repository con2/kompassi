import { redirect } from "next/navigation";

interface Props {
  params: Promise<{
    locale: string;
    eventSlug: string;
  }>;
}

export default async function ProgramsRedirectPage(props: Props) {
  const params = await props.params;
  const { eventSlug } = params;
  redirect(`/${eventSlug}/program`);
}
