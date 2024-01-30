"use client";

interface Props {
  subject: {
    canRemove: boolean;
  };
  messages: {
    title: string;
    cannotRemove: string;
    confirmation: string;
  };
}

export default function DeleteButton({ subject, messages }: Props) {
  const askForConfirmation = () => {
    return confirm(messages.confirmation);
  };

  if (!subject.canRemove) {
    return (
      <button
        disabled
        type="submit"
        className="btn btn-link btn-sm p-0 link-xsubtle"
        title={messages.cannotRemove}
        style={{ filter: "grayscale(100%)" }}
      >
        ❌
      </button>
    );
  }

  return (
    <button
      type="submit"
      className="btn btn-link btn-sm p-0 link-xsubtle"
      title={messages.title}
      onClick={askForConfirmation}
    >
      ❌
    </button>
  );
}
