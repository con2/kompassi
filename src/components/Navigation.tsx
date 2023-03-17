import Navbar from "react-bootstrap/Navbar";
import Container from "react-bootstrap/Container";

const Navigation = () => (
  <Navbar bg="dark" variant="dark" expand="lg" className="Navigation-Navbar">
    <Container fluid>
      <Navbar.Brand href="/">
        Kompassi<sup>v2 BETA</sup>
      </Navbar.Brand>
    </Container>
  </Navbar>
);

export default Navigation;
