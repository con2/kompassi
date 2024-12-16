import { ReactNode } from "react";

interface Props {
  title?: ReactNode;
  children?: ReactNode;
  className?: string;
}

export default function Section({ title, children, className }: Props) {
  className ??= "mb-4";

  return (
    <section className={className}>
      {title && <h3 className="mb-2">{title}</h3>}
      {children}
    </section>
  );
}
