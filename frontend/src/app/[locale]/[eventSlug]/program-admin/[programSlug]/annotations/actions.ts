"use server";

import { revalidatePath } from "next/cache";
import { updateProgramAnnotationsFromFormData } from "@/components/annotations/service";

export async function updateProgramAnnotations(
  locale: string,
  eventSlug: string,
  programSlug: string,
  annotationSlugs: string[],
  formData: FormData,
) {
  await updateProgramAnnotationsFromFormData(
    eventSlug,
    programSlug,
    formData,
    annotationSlugs,
  );

  revalidatePath(
    `/${locale}/${eventSlug}/program-admin/${programSlug}/annotations`,
  );
}
