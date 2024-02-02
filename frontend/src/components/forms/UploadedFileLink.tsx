interface Props {
  url: string;
}

export default function UploadedFileLink({ url }: Props) {
  const basename = decodeURI(new URL(url).pathname.split("/").pop() || "");
  return (
    <a href={url} target="_blank" rel="noreferrer noopener">
      {basename}
    </a>
  );
}
