import { t } from "../translations";

export default function SplashView() {
  return (
    <div className="p-5 mb-4 bg-light rounded-3">
      <div className="container-fluid py-5">
        <h1 className="display-5 fw-bold">{t((r) => r.Brand.appName)}</h1>
        <p className="col-md-8 fs-4">{t((r) => r.SplashView.engagement)}</p>
        <a className="btn btn-primary btn-lg" href="https://kompassi.eu">
          {t((r) => r.SplashView.backToKompassi)}…
        </a>
      </div>
    </div>
  );
}
