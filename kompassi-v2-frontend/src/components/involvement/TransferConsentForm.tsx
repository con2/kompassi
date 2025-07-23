import Card from "react-bootstrap/Card";
import CardBody from "react-bootstrap/CardBody";
import CardTitle from "react-bootstrap/CardTitle";
import FormattedDateTime from "../FormattedDateTime";
import { Field } from "../forms/models";
import { SchemaForm } from "../forms/SchemaForm";
import { ProfileFields } from "../profile/ProfileFields";
import { Registry } from "./models";
import { Scope } from "@/app/[locale]/[eventSlug]/program/models";
import { auth } from "@/auth";
import { Profile, ProfileFieldSelector } from "@/components/profile/models";
import { kompassiBaseUrl } from "@/config";
import type { Translations } from "@/translations/en";

function TransferDirectionArrow() {
  // XXX AI genenerated :) please do something to this
  return (
    <span className="m-2 d-inline-block rotate-sm-90">
      <svg
        width="1em"
        height="1em"
        viewBox="0 0 16 16"
        fill="currentColor"
        aria-hidden="true"
      >
        <path
          d="M4 8h8M8 4l4 4-4 4"
          stroke="currentColor"
          strokeWidth="2"
          fill="none"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
      <style>
        {`
          @media (max-width: 767.98px) {
            .rotate-sm-90 {
              transform: rotate(90deg);
            }
          }
        `}
      </style>
    </span>
  );
}

function RegistryComponent({
  registryType,
  registry,
  messages,
}: {
  registryType: string;
  registry: Registry;
  messages: Translations;
}) {
  const t = messages.TransferConsentForm;
  return (
    <Card className="flex-grow-1 w-100 w-md-auto">
      <CardBody>
        <div className="form-text mb-2">{registryType}:</div>
        <div className="fw-bold">{registry.title}</div>
        <div className="fst-italic">{registry.organization.name}</div>
        {registry.policyUrl ? (
          <div className="form-text mt-2">
            <a
              className="link-subtle"
              href={registry.policyUrl}
              target="_blank"
              rel="noopener noreferer"
            >
              {t.privacyPolicy}
            </a>
          </div>
        ) : (
          <div className="form-text mt-2">{t.privacyPolicyMissing}</div>
        )}
      </CardBody>
    </Card>
  );
}

interface Props {
  scope: Scope;
  profileFieldSelector: ProfileFieldSelector;
  profile: Profile;
  sourceRegistry: Registry;
  targetRegistry: Registry;
  translations: Translations;
  locale: string;
  className?: string;
  consentGivenAt?: string;
}

export default async function TransferConsentForm({
  scope,
  profileFieldSelector,
  profile,
  sourceRegistry,
  targetRegistry,
  consentGivenAt,
  translations,
  locale,
  className = "mt-4 mb-4 p-2 pb-0",
}: Props) {
  const t = translations.TransferConsentForm;
  const session = await auth();

  const fields: Field[] = [
    {
      slug: "kompassiTransferConsent",
      title: t.consentCheckBox,
      type: "SingleCheckbox",
      required: true,
    },
  ];

  return (
    <Card className={className}>
      <CardBody>
        <CardTitle>{t.title}</CardTitle>
        <div className="card-text">
          {consentGivenAt ? t.messageAlreadyAccepted : t.message}
        </div>
        <div className="d-flex flex-column flex-md-row align-items-center my-4">
          <RegistryComponent
            registryType={t.sourceRegistry}
            registry={sourceRegistry}
            messages={translations}
          />
          <TransferDirectionArrow />
          <RegistryComponent
            registryType={t.targetRegistry}
            registry={targetRegistry}
            messages={translations}
          />
        </div>
        <Card>
          <CardBody>
            <div className="form-text mb-2">{t.dataToBeTransferred}</div>
            <ProfileFields
              profileFieldSelector={profileFieldSelector}
              profile={profile}
              compact
              messages={translations.Profile}
            />
            <div className="form-text mt-2">
              {t.actions.editProfile.message}{" "}
              <a
                href={`${kompassiBaseUrl}/profile`}
                target="_blank"
                rel="noopener noreferrer"
                className="link-subtle"
              >
                {t.actions.editProfile.link}…
              </a>
            </div>
          </CardBody>
        </Card>
        {consentGivenAt ? (
          <div className="mt-4 mb-2">
            <em>
              {t.consentAlreadyGivenAt(
                <FormattedDateTime
                  value={consentGivenAt}
                  scope={scope}
                  session={session}
                  locale={locale}
                />,
              )}
            </em>
          </div>
        ) : (
          <SchemaForm
            className="mt-4"
            fields={fields}
            values={{}}
            messages={translations.SchemaForm}
          />
        )}
      </CardBody>
    </Card>
  );
}
