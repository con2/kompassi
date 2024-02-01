import useSWR from "swr";

export default function EventView() {
  const { data, error, isLoading } = useSWR<Event>(
    `/api/v3/events/${eventSlug}`,
    fetcher
  );
}
