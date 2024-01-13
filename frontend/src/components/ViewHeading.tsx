interface Props {
  children?: React.ReactNode;
}

export default function ViewHeading({ children }: Props) {
  return <h1 className="mb-3">{children}</h1>;
}

ViewHeading.Sub = function Sub({ children }: Props) {
  return (
    <>
      {" "}
      <span className="fs-5 text-muted">{children}</span>
    </>
  );
};
