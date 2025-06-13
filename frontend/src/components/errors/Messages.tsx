import { ReactNode } from "react";
import AlertNavigateOnClose from "./AlertNavigateOnClose";

interface Props {
  searchParams: {
    error?: string;
    success?: string;
  };
  messages: Record<string, string | ReactNode>;
}

/// An alert with one of the generic error messages.
export default function Messages({
  searchParams: { error, success } = {},
  messages: messages,
}: Props) {
  if (!error && !success) {
    return <></>;
  }

  let message: string | ReactNode = "";
  let variant: "success" | "danger" = "success";

  if (error) {
    message = messages[error];
    variant = "danger";
  } else if (success) {
    message = messages[success];
    variant = "success";
  }

  if (!message) {
    return <></>;
  }

  return (
    <AlertNavigateOnClose variant={variant}>{message}</AlertNavigateOnClose>
  );
}
