import { Field } from "../forms/models";
import { SchemaForm } from "../forms/SchemaForm";
import { Translations } from "@/translations/en";

interface Customer {
  firstName: string;
  lastName: string;
  email: string;
  phone: string;
}

interface Props {
  termsAndConditionsUrl?: string;
  messages: {
    Tickets: Translations["Tickets"];
    SchemaForm: Translations["SchemaForm"];
  };
  isAdmin?: boolean;
  values?: Customer;
  className?: string;
}

function getContactFormFields(
  t: Translations["Tickets"]["Order"],
  isAdmin: boolean,
  termsAndConditionsUrl?: string,
): Field[] {
  const fields: Field[] = [
    {
      slug: "firstName",
      type: "SingleLineText",
      required: true,
      title: t.attributes.firstName.title,
    },
    {
      slug: "lastName",
      type: "SingleLineText",
      required: true,
      title: t.attributes.lastName.title,
    },
    {
      slug: "email",
      type: "SingleLineText",
      required: true,
      title: t.attributes.email.title,
      helpText: isAdmin ? undefined : t.attributes.email.helpText,
    },
    {
      slug: "phone",
      type: "SingleLineText",
      title: t.attributes.phone.title,
    },
  ];

  if (termsAndConditionsUrl && !isAdmin) {
    fields.push({
      slug: "acceptTermsAndConditions",
      type: "SingleCheckbox",
      required: true,
      title: t.attributes.acceptTermsAndConditions.checkboxLabel(
        termsAndConditionsUrl,
      ),
    });
  }

  return fields;
}

export default function ContactForm({
  messages,
  isAdmin,
  values,
  className,
  termsAndConditionsUrl,
}: Props) {
  const fields = getContactFormFields(
    messages.Tickets.Order,
    !!isAdmin,
    termsAndConditionsUrl,
  );

  return (
    <SchemaForm
      fields={fields}
      values={values}
      messages={messages.SchemaForm}
      className={className}
    />
  );
}
