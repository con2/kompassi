import type { Translations } from "@/translations/en";
import Dropdown from "react-bootstrap/Dropdown";
import DropdownToggle from "react-bootstrap/DropdownToggle";
import DropdownMenu from "react-bootstrap/DropdownMenu";
import DropdownItem from "react-bootstrap/DropdownItem";

export interface ExportUrls {
  excel: string;
  zip: string;
}

interface Props {
  messages: Translations["Survey"]["actions"]["exportDropdown"];
  exportUrls: ExportUrls;
}

export default function ExportDropdown({ messages: t, exportUrls }: Props) {
  return (
    <Dropdown>
      <DropdownToggle variant="outline-primary" id="dropdown-basic">
        {t.dropdownHeader}…
      </DropdownToggle>

      <DropdownMenu>
        <DropdownItem href={exportUrls.excel}>{t.excel}</DropdownItem>
        <DropdownItem href={exportUrls.zip}>{t.zip}</DropdownItem>
      </DropdownMenu>
    </Dropdown>
  );
}
