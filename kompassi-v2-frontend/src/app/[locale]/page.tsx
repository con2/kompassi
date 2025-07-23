import { getTranslations, supportedLanguages } from "../../translations";
import { kompassiBaseUrl } from "@/config";

interface SplashViewProps {
  params: Promise<{
    locale: string;
  }>;
}

export function generateStaticParams() {
  return supportedLanguages.map((locale) => ({ locale }));
}

export default async function SplashView(props: SplashViewProps) {
  const params = await props.params;

  const { locale } = params;

  const translations = getTranslations(locale);

  return (
    <div className="p-5 mb-4 bg-body-tertiary rounded-3">
      <div className="container-fluid py-5">
        <h1 className="display-5 fw-bold">{translations.Brand.appName}</h1>
        <p className="col-md-8 fs-4">{translations.SplashView.engagement}</p>
        <a className="btn btn-primary btn-lg" href={kompassiBaseUrl}>
          {translations.SplashView.backToKompassi}…
        </a>
      </div>
    </div>
  );
}
