"use client";

import { useSearchParams } from "next/navigation";
import { useRouter } from "next/navigation";
import { useCallback } from "react";
import ToggleButton from "react-bootstrap/ToggleButton";

import type { Dimension, DimensionValue } from "./models";

interface PropsWithoutFavoriteFilter {
  dimensions: Dimension[];
  favoriteFilter?: false;
}

interface PropsWithFavoriteFilter {
  dimensions: Dimension[];
  favoriteFilter: true;
  messages: {
    showOnlyFavorites: string;
  };
}

type Props = PropsWithoutFavoriteFilter | PropsWithFavoriteFilter;

/// Presents the dimensions as dropdowns.
/// Updates the search params when the user selects a value.
/// Can be used in all use cases that follow the dimension pattern.
/// Gracefully degrades to showing a submit button when JavaScript is disabled.
export function DimensionFilters(props: Props) {
  const { dimensions, favoriteFilter } = props;
  const searchParams = useSearchParams();
  const { replace } = useRouter();

  const onChange = useCallback(
    (event: React.ChangeEvent<HTMLSelectElement>) => {
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
      const { name, checked } = event.target;
      const newSearchParams = new URLSearchParams(searchParams);

      if (checked) {
        newSearchParams.set(name, "1");
      } else {
        newSearchParams.delete(name);
      }

      const url = new URL(location.href);
      url.search = newSearchParams.toString();
      replace(url.toString());
    },
    [searchParams, replace],
  );

  return (
    <form className="row row-cols-md-auto g-3 align-items-center mb-3">
      {dimensions.map((dimension) => {
        const dimensionTitle = dimension.title ?? dimension.slug;
        const nothing: DimensionValue = {
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
              className="form-select form-select-sm border-secondary-subtle"
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
      {favoriteFilter && (
        <div className="col-12">
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
        </div>
      )}
      <noscript>
        <button type="submit" className="btn btn-sm btn-primary">
          Suodata
        </button>
      </noscript>
    </form>
  );
}
