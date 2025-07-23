interface Props {
  children?: React.ReactNode;
}

export default function ViewContainer({ children }: Props) {
  return <main className="container mt-4 mb-4">{children}</main>;
}
