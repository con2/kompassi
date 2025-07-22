import { redirect } from "next/navigation";

interface Props {
  params: Promise<{
    locale: string;
    eventSlug: string;
  }>;
}

export default async function OrdersRedirectPage(props: Props) {
  const params = await props.params;
  const { eventSlug } = params;
  return void redirect(`/profile/orders?event=${eventSlug}`);
}
