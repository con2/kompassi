"use client";

import { useSearchParams } from "next/navigation";
import { useRouter } from "next/navigation";
import { useCallback } from "react";

import type { Dimension, DimensionValue } from "../models";

interface Props {
  dimensions: Dimension[];
}

/// Presents the dimensions as dropdowns.
/// Updates the search params when the user selects a value.
/// Can be used in all use cases that follow the dimension pattern.
/// Gracefully degrades to showing a submit button when JavaScript is disabled.
export function DimensionFilters({ dimensions }: Props) {
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

  return (
    <form className="row row-cols-lg-auto g-3 align-items-center mb-3">
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
              className="form-select form-select-sm"
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
      <noscript>
        <button type="submit" className="btn btn-sm btn-primary">
          Suodata
        </button>
      </noscript>
    </form>
  );
}
