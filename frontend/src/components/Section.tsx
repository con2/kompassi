interface Props {
  title: string;
  children?: React.ReactNode;
  className?: string;
}

export default function Section({ title, children, className }: Props) {
  className ??= "mb-4";

  return (
    <section className={className}>
      <h2 className="mb-2">{title}</h2>
      {children}
    </section>
  );
}
