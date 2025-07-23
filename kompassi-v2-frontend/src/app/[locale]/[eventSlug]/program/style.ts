import { ScheduleProgramFragment } from "@/__generated__/graphql";

export function getProgramColorBorder(program: ScheduleProgramFragment) {
  const borderLeftColor = program.color ?? "var(--bs-border-color-translucent)";
  return {
    borderLeft: `4px solid ${borderLeftColor}`,
  };
}
