import { Profile, profileFields, ProfileFieldSelector } from "./models";
import type { Translations } from "@/translations/en";

interface Props {
  profileFieldSelector: ProfileFieldSelector;
  profile: Profile;
  className?: string;
  fieldClassName?: string;
  compact?: boolean;
  messages: Translations["Profile"];
}

export function ProfileFields({
  profileFieldSelector,
  profile,
  compact = false,
  className = "mb-3 mt-3",
  fieldClassName = "mb-2",
  messages: t,
}: Props) {
  if (compact) {
    className = `row ${className}`;
    fieldClassName = `col-12 col-md-4 ${fieldClassName}`;
  }

  return (
    <div className={className}>
      {profileFields
        .filter((field) => profileFieldSelector[field])
        .map((field) => {
          return (
            <div key={field} className={fieldClassName}>
              <div className="form-label fw-bold">{t.attributes[field]}</div>
              <div>{profile[field]}</div>
            </div>
          );
        })}
    </div>
  );
}
