import Navbar from "react-bootstrap/Navbar";
import Nav from "react-bootstrap/Nav";
import Container from "react-bootstrap/Container";
import { detectedLanguage, setLanguage, t } from "../translations";
import { useCallback } from "react";

const Navigation = () => {
  const otherLanguageCode = detectedLanguage == "en" ? "fi" : "en";
  const otherLanguageName = t((r) => r.LanguageSelection[otherLanguageCode]);
  const toggleLanguage = useCallback(
    () => setLanguage(otherLanguageCode),
    [otherLanguageCode]
  );
  return (
    <Navbar bg="dark" variant="dark" expand="lg" className="Navigation-Navbar">
      <Container fluid>
        <Navbar.Brand href="/">{t((r) => r.Brand.appName)}</Navbar.Brand>
        <Navbar.Toggle />
        <Navbar.Collapse>
          <Nav className="ms-auto">
            <Nav.Link onClick={toggleLanguage}>{otherLanguageName}</Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default Navigation;
