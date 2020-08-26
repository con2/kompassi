import React from 'react';

import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Container from 'react-bootstrap/Container';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';

import CharacterTextEditor from './CharacterTextEditor';

interface Character {
  publicName: string;
}

export default function ContactEditor() {
  const character: Character = {
    publicName: 'Aarne Aarnela',
  };
  const otherCharacter: Character = {
    publicName: 'Bertta Berttanen',
  };

  return (
    <Container fluid>
      <h2>
        Kontakti{' '}
        <small className="text-muted">
          {character.publicName} ↔ {otherCharacter.publicName}
        </small>
      </h2>
      <Row>
        <Col>
          <Card>
            <Card.Body>
              <Card.Title>Julkinen lyhäri {character.publicName}</Card.Title>
              <CharacterTextEditor />
            </Card.Body>
          </Card>
        </Col>
        <Col>
          <Card>
            <Card.Body>
              <Card.Title>Kontakti profiilissa {character.publicName}</Card.Title>
              <CharacterTextEditor />
            </Card.Body>
          </Card>
        </Col>
        <Col>
          <Card>
            <Card.Body>
              <Card.Title>Kontakti profiilissa {otherCharacter.publicName}</Card.Title>
              <CharacterTextEditor />
            </Card.Body>
          </Card>
        </Col>
        <Col>
          <Card>
            <Card.Body>
              <Card.Title>Julkinen lyhäri {otherCharacter.publicName}</Card.Title>
              <CharacterTextEditor />
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
}
