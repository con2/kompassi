"use client";

import { useContext } from "react";
import Button from "react-bootstrap/Button";
import classes from "./FavoriteButton.module.css";
import { FavoriteContext } from "./FavoriteContext";

interface Props {
  slug: string;
  size?: "lg" | "xl";
}

export default function FavoriteButton({ slug, size }: Props) {
  const { markAsFavorite, unmarkAsFavorite, isFavorite, messages } =
    useContext(FavoriteContext);

  const thisIsFavorite = isFavorite(slug);
  const cssClasses = thisIsFavorite
    ? [classes.favorite, classes.active]
    : [classes.favorite];

  if (size === "xl") {
    cssClasses.push(classes.xl);
  }

  const toggleFavorite = thisIsFavorite
    ? () => unmarkAsFavorite(slug)
    : () => markAsFavorite(slug);

  const title = thisIsFavorite
    ? messages.unmarkAsFavorite
    : messages.markAsFavorite;

  return (
    <Button
      type="submit"
      variant="link"
      className={cssClasses.join(" ")}
      title={title}
      onClick={toggleFavorite}
    >
      ⭐
    </Button>
  );
}
