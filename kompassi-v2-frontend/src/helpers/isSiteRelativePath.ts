/// A "use server" actions file may only export async functions, so this plain helper
/// lives on its own: it validates a `next` redirect target that arrives from a query
/// string (leading `/`, no scheme, no `//`) before the sudo page/action ever redirects to it.
export default function isSiteRelativePath(path: string): boolean {
  return path.startsWith("/") && !path.startsWith("//");
}
