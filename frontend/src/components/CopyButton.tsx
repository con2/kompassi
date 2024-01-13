"use client";

interface Props {
  data: string;
  className?: string;
  messages: {
    title: string;
    tooltip?: string;
    success: string;
  };
}

export default function CopyButton({ data, className, messages }: Props) {
  className ??= "btn btn-outline-primary";

  // a button that copies data to clipboard when clicked
  return (
    <button
      className={className}
      title={messages.tooltip}
      onClick={() => {
        navigator.clipboard.writeText(data);

        // TODO use a toast or a popover instead
        alert(messages.success);
      }}
    >
      {messages.title}…
    </button>
  );
}
