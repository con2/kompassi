"use client";

import { ReactNode } from "react";
import { ButtonGroup } from "react-bootstrap";
import Dropdown from "react-bootstrap/Dropdown";
import SubscriptionButton from "./SubscriptionButton";
import type { Translations } from "@/translations/en";
import ExportDropdown, { ExportUrls } from "./ExportDropdown";

interface Messages {
  toggleSubscription: string;
  exportDropdown: Translations["Survey"]["actions"]["exportDropdown"];
}

interface Props {
  isSubscribed: boolean;
  onToggleSubscription(): Promise<void>;
  exportUrls: ExportUrls;
  messages: Messages;
  children: ReactNode;
}

export function ResponseListActions({
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

      <ExportDropdown
        messages={messages.exportDropdown}
        exportUrls={exportUrls}
      />
    </Dropdown>
  );
}
