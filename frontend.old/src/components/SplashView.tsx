import Container from "react-bootstrap/Container";
import Button from "react-bootstrap/Button";

import { t } from "../translations";

export default function SplashView() {
  return (
    <div className="p-5 mb-4 bg-light rounded-3">
      <Container fluid className="py-5">
        <h1 className="display-5 fw-bold">{t((r) => r.Brand.appName)}</h1>
        <p className="col-md-8 fs-4">{t((r) => r.SplashView.engagement)}</p>
        <Button href="https://kompassi.eu" size="lg">
          {t((r) => r.SplashView.backToKompassi)}…
        </Button>
      </Container>
    </div>
  );
}
