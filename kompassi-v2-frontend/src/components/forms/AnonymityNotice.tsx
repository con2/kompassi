import Card from "react-bootstrap/Card";
import CardBody from "react-bootstrap/CardBody";
import CardTitle from "react-bootstrap/CardTitle";

import { Anonymity } from "@/__generated__/graphql";
import { ProfileFields } from "@/components/profile/ProfileFields";
import {
  Profile,
  profileFields,
  ProfileFieldSelector,
} from "@/components/profile/models";
import type { Translations } from "@/translations/en";

interface Props {
  anonymity: Anonymity;
  profileFieldSelector: ProfileFieldSelector;
  profile?: Profile | null;
  messages: Translations;
  className?: string;
}

export function AnonymityNotice({
  anonymity,
  profileFieldSelector,
  profile,
  messages: translations,
  className = "mt-4 mb-4 p-2",
}: Props) {
  const t = translations.Survey.attributes.anonymity.secondPerson;
  const hasSelectedFields = profileFields.some((f) => profileFieldSelector[f]);

  return (
    <Card className={className}>
      <CardBody>
        <CardTitle>{t.title}</CardTitle>
        <div className="card-text">{t.choices[anonymity]}</div>
        {hasSelectedFields && profile && (
          <Card className="mt-3">
            <CardBody>
              <ProfileFields
                profileFieldSelector={profileFieldSelector}
                profile={profile}
                compact
                messages={translations.Profile}
              />
            </CardBody>
          </Card>
        )}
      </CardBody>
    </Card>
  );
}
