import { getTranslations, supportedLanguages } from "../../translations";

interface SplashViewProps {
  params: {
    locale: string;
  };
}

export function generateStaticParams() {
  return supportedLanguages.map((locale) => ({ locale }));
}

export default function SplashView({ params: { locale }}: SplashViewProps) {
  const translations = getTranslations(locale);

  return (
    <div className="p-5 mb-4 bg-light rounded-3">
      <div className="container-fluid py-5">
        <h1 className="display-5 fw-bold">{translations.Brand.appName}</h1>
        <p className="col-md-8 fs-4">{translations.SplashView.engagement}</p>
        <a className="btn btn-primary btn-lg" href="https://kompassi.eu">
          {translations.SplashView.backToKompassi}…
        </a>
      </div>
    </div>
  );
}
