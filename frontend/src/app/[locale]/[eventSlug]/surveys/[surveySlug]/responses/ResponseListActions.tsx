"use client";

import { ReactNode } from "react";
import { ButtonGroup } from "react-bootstrap";
import Dropdown from "react-bootstrap/Dropdown";
import SubscriptionButton from "./SubscriptionButton";
import type { Translations } from "@/translations/en";

interface Messages {
  toggleSubscription: string;
  exportDropdown: Translations["Survey"]["actions"]["exportDropdown"];
}

interface Props {
  scope: {
    slug: string;
  };
  survey: {
    slug: string;
  };
  isSubscribed: boolean;
  onToggleSubscription(): Promise<void>;
  exportUrls: {
    excel: string;
    zip: string;
  };
  messages: Messages;
  children: ReactNode;
}

export function ResponseListActions({
  scope,
  survey,
  isSubscribed,
  onToggleSubscription,
  exportUrls,
  messages,
  children,
}: Props) {
  return (
    <Dropdown as={ButtonGroup}>
      <SubscriptionButton
        initialChecked={isSubscribed}
        onChange={onToggleSubscription}
      >
        {messages.toggleSubscription}
      </SubscriptionButton>

      {children}

      <Dropdown.Toggle variant="outline-primary" id="dropdown-basic">
        {messages.exportDropdown.dropdownHeader}…
      </Dropdown.Toggle>

      <Dropdown.Menu>
        <Dropdown.Item href={exportUrls.excel}>
          {messages.exportDropdown.excel}
        </Dropdown.Item>
        <Dropdown.Item href={exportUrls.zip}>
          {messages.exportDropdown.zip}
        </Dropdown.Item>
      </Dropdown.Menu>
    </Dropdown>
  );
}
