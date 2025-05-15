import Card from "react-bootstrap/Card";
import CardBody from "react-bootstrap/CardBody";
import CardHeader from "react-bootstrap/CardHeader";
import CardText from "react-bootstrap/CardText";
import CardTitle from "react-bootstrap/CardTitle";
import { Field } from "../forms/models";
import { SchemaForm } from "../forms/SchemaForm";
import {
  Profile,
  ProfileField,
  profileFields,
  ProfileFieldSelector,
  Registry,
} from "./models";
import type { Translations } from "@/translations/en";

interface Messages {
  TransferConsentForm: {
    title: string; // Transfer of personal data
    message: string; // When you fill in this form…
    consentCheckBox: string; // I consent to the …
    privacyPolicy: string; // Privacy policy
    actions: {
      editProfile: string; // If you notice any mistakes…
    };
    sourceRegistry: string; // Source of the data
    targetRegistry: string; // Receiver of the data
  };
  Profile: {
    attributes: Record<ProfileField, string>; // {firstName: "First name", lastName: "Last name", ...}
  };
  SchemaForm: Translations["SchemaForm"];
}

interface Props {
  profileFieldSelector: ProfileFieldSelector;
  profile: Profile;
  sourceRegistry: Registry;
  targetRegistry: Registry;
  messages: Messages;
}

function RightArrow() {
  return (
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
  );
}

function RegistryComponent({
  registryType,
  registry,
  messages,
}: {
  registryType: string;
  registry: Registry;
  messages: Messages;
}) {
  const t = messages.TransferConsentForm;
  return (
    <div className="flex-grow-1">
      <CardText>
        <div className="form-text">{registryType}:</div>
        <div className="fw-bold">{registry.title}</div>
        <div className="fst-italic">{registry.organization.name}</div>
        <div>
          <a
            href={registry.privacyPolicyUrl}
            target="_blank"
            rel="noopener noreferer"
          >
            {t.privacyPolicy}
          </a>
        </div>
      </CardText>
    </div>
  );
}

export default function TransferConsentForm({
  profileFieldSelector,
  profile,
  sourceRegistry,
  targetRegistry,
  messages,
}: Props) {
  const t = messages.TransferConsentForm;

  const consentFields: Field[] = [
    {
      slug: "consent",
      title: t.consentCheckBox,
      type: "SingleCheckbox",
      required: true,
    },
  ];

  return (
    <Card>
      <CardHeader>
        <CardTitle>{t.title}</CardTitle>
      </CardHeader>
      <CardBody>
        <CardText>{t.message}</CardText>
        <div className="d-flex align-items-center">
          <RegistryComponent
            registryType={t.sourceRegistry}
            registry={sourceRegistry}
            messages={messages}
          />
          <RightArrow />
          <RegistryComponent
            registryType={t.targetRegistry}
            registry={targetRegistry}
            messages={messages}
          />
        </div>
        {profileFields.map((field) => {
          if (!profileFieldSelector[field]) {
            return null;
          }
          return (
            <div key={field} className="mb-1">
              <div>
                <strong>{messages.Profile.attributes[field]}</strong>
              </div>
              <div>{(profile as any)[field]}</div>
            </div>
          );
        })}
        <SchemaForm
          fields={consentFields}
          values={{}}
          messages={messages.SchemaForm}
        />
      </CardBody>
    </Card>
  );
}
