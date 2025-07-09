import { redirect } from "next/navigation";

interface Props {
  params: {
    locale: string;
    eventSlug: string;
  };
}

export default function OrdersRedirectPage({ params }: Props) {
  const { eventSlug } = params;
  return void redirect(`/profile/orders?event=${eventSlug}`);
}
