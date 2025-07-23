"use client";

import { ReactNode } from "react";
import { getProductEntries } from "@/services/tickets";
import type { Translations } from "@/translations/en";

interface Props {
  messages: {
    NO_PRODUCTS_SELECTED: Translations["Tickets"]["Order"]["errors"]["NO_PRODUCTS_SELECTED"];
  };
  children?: ReactNode;

  onSubmit(formData: FormData): Promise<void>;
}

/// Responsible for validating that there is at least one product.
/// Gracefully degrades if JavaScript is disabled.
export default function ProductsForm({ messages, onSubmit, children }: Props) {
  function handleSubmit(formData: FormData) {
    if (getProductEntries(formData).length === 0) {
      // TODO some better way to show this (setCustomValidity?)
      alert(messages.NO_PRODUCTS_SELECTED.message);
      return;
    }

    onSubmit(formData);
  }

  return <form action={handleSubmit}>{children}</form>;
}
