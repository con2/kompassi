import type { Translations } from "@/translations/en";

export function extractBasenameFromPresignedUrl(url: string) {
  const urlObj = new URL(url);
  return urlObj.pathname.split("/").pop();
}

interface Props {
  urls?: string[];
  messages: Translations["SchemaForm"];
}

export default function UploadedFileCards({ urls, messages }: Props) {
  if (!urls || urls.length === 0) {
    return (
      <div className="card mb-2">
        <div className="card-body p-2 ps-3 pe-3">
          <em className="text-muted">{messages.warnings.noFileUploaded}</em>
        </div>
      </div>
    );
  }

  // value is a list of presigned S3 URLs
  return (
    <>
      {urls.map((url, idx) => {
        const basename = extractBasenameFromPresignedUrl(url);
        return (
          <div key={idx} className="card mb-2">
            <div className="card-body p-2 ps-3 pe-3">
              <a href={url} target="_blank" rel="noreferrer">
                {basename}
              </a>
            </div>
          </div>
        );
      })}
    </>
  );
}
