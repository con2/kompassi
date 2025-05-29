"use client";

import { usePathname, useRouter } from "next/navigation";
import { ReactNode } from "react";
import Alert from "react-bootstrap/Alert";
import { Variant } from "react-bootstrap/esm/types";

interface Props {
  href?: string;
  variant: Variant;
  children: ReactNode;
}

/// When an Alert is triggered by a server action and communicated via eg. a query string parameter,
/// this component can be used to clear the query string parameter when the Alert is closed.
export default function AlertNavigateOnClose({
  href,
  children,
  variant = "success",
}: Props) {
  const router = useRouter();
  const path = usePathname();
  const alwaysHref = href || path;

  return (
    <Alert
      variant={variant}
      dismissible
      onClose={() => router.replace(alwaysHref)}
    >
      {children}
    </Alert>
  );
}
