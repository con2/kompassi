import Section from "@/components/Section";
import type { Translations } from "@/translations/en";

interface Seller {
  name: string;
  email?: string | null;
  businessId?: string | null;
}

interface Props {
  seller: Seller;
  messages: Translations["Tickets"]["Order"]["attributes"]["seller"];
}

export default function SellerSection({ seller, messages: t }: Props) {
  return (
    <Section>
      <div>
        <strong>{t.title}</strong>: {seller.name}
      </div>
      {seller.email && (
        <div>
          <strong>{t.email}</strong>:{" "}
          <a href={`mailto:${seller.email}`}>{seller.email}</a>
        </div>
      )}
      {seller.businessId && (
        <div>
          <strong>{t.businessId}</strong>: {seller.businessId}
        </div>
      )}
    </Section>
  );
}
