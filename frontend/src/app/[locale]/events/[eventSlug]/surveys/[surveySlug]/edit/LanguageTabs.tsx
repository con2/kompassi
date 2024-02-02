"use client";

import Tab from "react-bootstrap/Tab";
import Tabs from "react-bootstrap/Tabs";
import type { Translations } from "@/translations/en";

interface Props {
  messages: Translations["Survey"]["editFormTabs"];
}

export default function LanguageTabs({ messages }: Props) {
  return (
    <Tabs defaultActiveKey="new" id="survey-tabs">
      <Tab
        eventKey="new"
        title={`➕ ${messages.actions.addLanguageVersion}…`}
      ></Tab>
    </Tabs>
  );
}
