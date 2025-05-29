import { ReactNode } from "react";
import AlertNavigateOnClose from "./AlertNavigateOnClose";

interface Props {
  error: string | null | undefined;
  messages: Record<string, string | ReactNode>;
}

/// An alert with one of the generic error messages.
export default function Errors({ error, messages }: Props) {
  if (!error) {
    return <></>;
  }

  return (
    <AlertNavigateOnClose variant="danger">
      {messages[error] || messages["default"] || error}
    </AlertNavigateOnClose>
  );
}
