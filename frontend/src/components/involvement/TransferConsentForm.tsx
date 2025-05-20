import Card from "react-bootstrap/Card";
import CardBody from "react-bootstrap/CardBody";
import CardTitle from "react-bootstrap/CardTitle";
import { Field } from "../forms/models";
import { SchemaForm } from "../forms/SchemaForm";
import {
  Profile,
  profileFields,
  ProfileFieldSelector,
  Registry,
} from "./models";
import { kompassiBaseUrl } from "@/config";
import type { Translations } from "@/translations/en";

function TransferDirectionArrow() {
  // XXX AI genenerated :) please do something to this
  return (
    <span className="mx-2 d-inline-block rotate-sm-90">
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
    <Card className="flex-grow-1 m-3">
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
  profileFieldSelector: ProfileFieldSelector;
  profile: Profile;
  sourceRegistry: Registry;
  targetRegistry: Registry;
  translations: Translations;
  className?: string;
}

export default function TransferConsentForm({
  profileFieldSelector,
  profile,
  sourceRegistry,
  targetRegistry,
  translations: messages,
  className = "mt-4 mb-4",
}: Props) {
  const t = messages.TransferConsentForm;

  const consentFields: Field[] = [
    {
      slug: "kompassi_transfer_consent",
      title: t.consentCheckBox,
      type: "SingleCheckbox",
      required: true,
    },
  ];

  return (
    <Card className={className}>
      <CardBody>
        <CardTitle>{t.title}</CardTitle>
        <div className="card-text">{t.message}</div>
        <div className="d-flex flex-column flex-md-row align-items-center">
          <RegistryComponent
            registryType={t.sourceRegistry}
            registry={sourceRegistry}
            messages={messages}
          />
          <TransferDirectionArrow />
          <RegistryComponent
            registryType={t.targetRegistry}
            registry={targetRegistry}
            messages={messages}
          />
        </div>
        <Card className="m-3">
          <CardBody>
            <div className="form-text mb-2">Luovutettavat tiedot:</div>
            {profileFields.map((field) => {
              if (!profileFieldSelector[field]) {
                return null;
              }
              return (
                <div key={field} className="mb-2">
                  <div>
                    <strong>{messages.Profile.attributes[field]}</strong>
                  </div>
                  <div>{(profile as any)[field]}</div>
                </div>
              );
            })}
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
        <SchemaForm
          className="mt-4"
          fields={consentFields}
          values={{}}
          messages={messages.SchemaForm}
        />
      </CardBody>
    </Card>
  );
}
