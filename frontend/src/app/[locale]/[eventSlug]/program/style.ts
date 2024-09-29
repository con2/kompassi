import { ProgramListFragment } from "@/__generated__/graphql";

export function getProgramColorBorder(program: ProgramListFragment) {
  const borderLeftColor = program.color ?? "var(--bs-border-color-translucent)";
  return {
    borderLeft: `4px solid ${borderLeftColor}`,
  };
}
