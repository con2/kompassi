"use client";

import { Temporal } from "@js-temporal/polyfill";
import { Button } from "react-bootstrap";

import { ReportFragment } from "@/__generated__/graphql";
import type { Translations } from "@/translations/en";

import { reportCsvFilename, reportToCsv } from "./reportCsv";

interface Props {
  report: ReportFragment;
  filenamePrefix: string;
  timezone: Temporal.TimeZoneLike;
  messages: Translations["Report"]["actions"];
}

export default function ReportCsvDownloadButton({
  report,
  filenamePrefix,
  timezone,
  messages,
}: Props) {
  function download() {
    const blob = new Blob([reportToCsv(report)], {
      type: "text/csv;charset=utf-8",
    });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = reportCsvFilename(report, filenamePrefix, timezone);
    link.click();
    URL.revokeObjectURL(url);
  }

  return (
    <Button variant="outline-primary" size="sm" onClick={download}>
      {messages.downloadCsv}
    </Button>
  );
}
