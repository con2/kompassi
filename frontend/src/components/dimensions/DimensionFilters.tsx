"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { useCallback } from "react";
import ButtonGroup from "react-bootstrap/ButtonGroup";
import ToggleButton from "react-bootstrap/ToggleButton";

import classes from "./DimensionFilters.module.css";
import {
  DimensionFilterFragment,
  DimensionFilterValueFragment,
} from "@/__generated__/graphql";

interface PropsWithoutProgramFilters {
  programFilters?: false;
  className?: string;
  search?: boolean;
  dimensions: DimensionFilterFragment[];
  messages?: {
    searchPlaceholder?: string;
  };
}

interface PropsWithProgramFilters {
  programFilters: true;
  className?: string;
  search?: boolean;
  dimensions: DimensionFilterFragment[];
  isLoggedIn: boolean;
  messages: {
    showOnlyFavorites?: string;
    hidePastPrograms?: string;
    searchPlaceholder?: string;
  };
}

type Props = PropsWithoutProgramFilters | PropsWithProgramFilters;

/// Presents the dimensions as dropdowns.
/// Updates the search params when the user selects a value.
/// Can be used in all use cases that follow the dimension pattern.
/// Gracefully degrades to showing a submit button when JavaScript is disabled.
export function DimensionFilters(props: Props) {
  const { dimensions, programFilters, search, messages } = props;
  const searchParams = useSearchParams();
  const searchTerm = search ? searchParams.get("search") ?? "" : "";
  const { replace } = useRouter();

  const onChange = useCallback(
    (
      event:
        | React.ChangeEvent<HTMLSelectElement>
        | React.FocusEvent<HTMLInputElement>,
    ) => {
      // update searchParams and navigate to it
      const { name, value } = event.target;
      const newSearchParams = new URLSearchParams(searchParams);

      if (value === "") {
        newSearchParams.delete(name);
      } else {
        newSearchParams.set(name, value);
      }

      const url = new URL(location.href);
      url.search = newSearchParams.toString();
      replace(url.toString());
    },
    [searchParams, replace],
  );

  const onChangeFavorite = useCallback(
    (event: React.ChangeEvent<HTMLInputElement>) => {
      const { name, checked, value } = event.target;
      const newSearchParams = new URLSearchParams(searchParams);

      if (checked) {
        newSearchParams.set(name, value);
      } else {
        newSearchParams.delete(name);
      }

      const url = new URL(location.href);
      url.search = newSearchParams.toString();
      replace(url.toString());
    },
    [searchParams, replace],
  );

  // For clients with JavaScript, do a soft navigation on submit.
  // Clients without JavaScript still degrade gracefully to a full page reload.
  const onSubmit = useCallback(
    (event: React.FormEvent<HTMLFormElement>) => {
      event.preventDefault();
      const form = event.currentTarget;
      const newSearchParams = new URLSearchParams(searchParams);

      for (const element of form.elements as any) {
        if (element.name && element.value) {
          newSearchParams.set(element.name, element.value);
        } else {
          newSearchParams.delete(element.name);
        }
      }

      const url = new URL(location.href);
      url.search = newSearchParams.toString();
      replace(url.toString());
    },
    [searchParams, replace],
  );

  const className = `row row-cols-md-auto g-3 align-items-center mt-1 mb-2 ${
    props.className ?? ""
  }`;

  return (
    <form className={className} onSubmit={onSubmit}>
      {dimensions.map((dimension) => {
        const dimensionTitle = dimension.title ?? dimension.slug;
        const nothing: DimensionFilterValueFragment = {
          slug: "",
          title: `${dimensionTitle}...`,
        };
        const choices = [nothing].concat(dimension.values);
        const inputId = `dimension-${dimension.slug}`;
        const selectedSlug = searchParams.get(dimension.slug) ?? "";

        return (
          <div className="col-12" key={dimension.slug}>
            <label className="visually-hidden" htmlFor={inputId}>
              {dimension.title}
            </label>
            <select
              name={dimension.slug}
              id={inputId}
              className={`form-select form-select-sm border-secondary-subtle ${classes.dimensionFilter}`}
              defaultValue={selectedSlug}
              onChange={onChange}
            >
              {choices.map((choice) => (
                <option key={choice.slug} value={choice.slug}>
                  {choice.title}
                </option>
              ))}
            </select>
          </div>
        );
      })}
      {search && (
        <div className="col-12">
          <input
            className={`form-control form-control-sm border-secondary-subtle ${classes.searchTerm}`}
            defaultValue={searchTerm}
            placeholder={
              messages?.searchPlaceholder && messages.searchPlaceholder + "…"
            }
            onBlur={onChange}
            name="search"
          />
        </div>
      )}
      {programFilters && (
        <ButtonGroup className="col-12 ms-auto">
          {props.isLoggedIn && (
            <ToggleButton
              variant="outline-primary"
              className="border-secondary-subtle"
              type="checkbox"
              id="favorites-only"
              value="1"
              size="sm"
              onChange={onChangeFavorite}
              name="favorited"
              checked={!!searchParams.get("favorited")}
              title={props.messages.showOnlyFavorites}
            >
              ⭐
            </ToggleButton>
          )}
          <ToggleButton
            variant="outline-primary"
            className="border-secondary-subtle"
            type="checkbox"
            id="hide-past-programs"
            value="0"
            size="sm"
            onChange={onChangeFavorite}
            name="past"
            checked={!!searchParams.get("past")}
            title={props.messages.hidePastPrograms}
          >
            🕒
          </ToggleButton>
        </ButtonGroup>
      )}
      <noscript>
        <button type="submit" className="btn btn-sm btn-primary">
          Suodata
        </button>
      </noscript>
    </form>
  );
}
