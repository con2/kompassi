interface Props {
  params: {
    locale: string;
    eventSlug: string;
    invitationId: string;
  };
}

export default function InvitationPage({ params }: Props) {
  const { locale, eventSlug, invitationId } = params;

  return (
    <div>
      <h1>Invitation Page</h1>
      <p>Locale: {locale}</p>
      <p>Event Slug: {eventSlug}</p>
      <p>Invitation ID: {invitationId}</p>
    </div>
  );
}
