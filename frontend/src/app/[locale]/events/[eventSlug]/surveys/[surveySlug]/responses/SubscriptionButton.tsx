"use client";

import { ReactNode, useCallback, useState } from "react";
import ToggleButton from "react-bootstrap/ToggleButton";

interface Props {
  initialChecked: boolean;
  onChange(checked: boolean): void;
  children?: ReactNode;
}

export default function SubscriptionButton({
  initialChecked,
  onChange,
  children,
}: Props) {
  const [checked, setChecked] = useState(initialChecked);
  const handleChange = useCallback(
    (event: React.ChangeEvent<HTMLInputElement>) => {
      setChecked(event.currentTarget.checked);
      onChange(event.currentTarget.checked);
    },
    [onChange],
  );

  return (
    <ToggleButton
      id="survey-subscribe-toggle-button"
      name="subscribe"
      value="1"
      type="checkbox"
      checked={checked}
      variant="outline-primary"
      onChange={handleChange}
    >
      {children}
    </ToggleButton>
  );
}
