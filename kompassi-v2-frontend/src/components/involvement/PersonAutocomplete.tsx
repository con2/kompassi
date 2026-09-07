"use client";

import { SubmitButton } from "@con2/components";
import { useEffect, useState, useTransition } from "react";
import Form from "react-bootstrap/Form";
import ListGroup from "react-bootstrap/ListGroup";

export interface PersonOption {
  id: string;
  fullName: string;
  nick: string;
}

function formatPerson(person: PersonOption): string {
  return person.nick ? `${person.fullName} (${person.nick})` : person.fullName;
}

interface Messages {
  placeholder: string;
  searching: string;
  noResults: string;
  clear: string;
}

interface Props {
  search: (query: string) => Promise<PersonOption[]>;
  name?: string;
  minLength?: number;
  messages: Messages;
  submitLabel: string;
}

export default function PersonAutocomplete({
  search,
  name = "personId",
  minLength = 2,
  messages,
  submitLabel,
}: Props) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<PersonOption[]>([]);
  const [selected, setSelected] = useState<PersonOption | null>(null);
  const [isPending, startTransition] = useTransition();

  const isSearching = !selected && query.length >= minLength;

  useEffect(() => {
    if (!isSearching) {
      return;
    }

    const timeout = setTimeout(() => {
      startTransition(async () => {
        setResults(await search(query));
      });
    }, 300);

    return () => clearTimeout(timeout);
  }, [query, isSearching, search]);

  const open = isSearching;

  function handleQueryChange(value: string) {
    setQuery(value);
    setSelected(null);
    setResults([]);
  }

  function selectPerson(person: PersonOption) {
    setSelected(person);
    setQuery(formatPerson(person));
  }

  function clearSelection() {
    setSelected(null);
    setQuery("");
    setResults([]);
  }

  return (
    <div className="d-flex gap-2 align-items-start">
      <div className="position-relative flex-grow-1">
        <Form.Control
          type="text"
          autoComplete="off"
          placeholder={messages.placeholder}
          value={query}
          disabled={!!selected}
          onChange={(event) => handleQueryChange(event.target.value)}
        />
        {open && (
          <ListGroup
            className="position-absolute w-100"
            style={{ zIndex: 1000 }}
          >
            {isPending && (
              <ListGroup.Item disabled>{messages.searching}</ListGroup.Item>
            )}
            {!isPending && results.length === 0 && (
              <ListGroup.Item disabled>{messages.noResults}</ListGroup.Item>
            )}
            {!isPending &&
              results.map((person) => (
                <ListGroup.Item
                  key={person.id}
                  action
                  onMouseDown={() => selectPerson(person)}
                >
                  {formatPerson(person)}
                </ListGroup.Item>
              ))}
          </ListGroup>
        )}
        <input type="hidden" name={name} value={selected?.id ?? ""} />
      </div>
      {selected && (
        <button
          type="button"
          className="btn btn-outline-secondary"
          onClick={clearSelection}
        >
          {messages.clear}
        </button>
      )}
      <SubmitButton disabled={!selected}>{submitLabel}</SubmitButton>
    </div>
  );
}
