import Container from "react-bootstrap/Container";
import Button from "react-bootstrap/Button";

import { T } from "../translations";

export default function SplashView() {
  const t = T((r) => r.SplashView);

  return (
    <div className="p-5 mb-4 bg-light rounded-3">
      <Container fluid className="py-5">
        <h1 className="display-5 fw-bold">
          Kompassi<sup>v2 BETA</sup>
        </h1>
        <p className="col-md-8 fs-4">{t((r) => r.engagement)}</p>
        <Button href="https://kompassi.eu" target="_blank" size="lg">
          kompassi.eu
        </Button>
      </Container>
    </div>
  );
}
