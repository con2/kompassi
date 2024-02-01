import useSWR from "swr";
import { useTable, Column } from "react-table";

import MainViewContainer from "../common/MainViewContainer";
import { Table } from "react-bootstrap";
import { T } from "../../translations";
import Event from "./Event";

const fetcher = (url: string) => fetch(url).then((res) => res.json());

const columns: Column<Event>[] = [
  {
    Header: "Name",
    accessor: "name",
    Cell: ({ row, value }) => (
      <a href={`/events/${row.original.slug}`}>{value}</a>
    ),
  },
  {
    Header: "Headline",
    accessor: "headline",
  },
];

export default function EventsView() {
  const { data, error, isLoading } = useSWR<Event[]>("/api/v3/events", fetcher);

  const { getTableProps, headerGroups, rows, prepareRow } = useTable({
    columns,
    data: data ?? [],
  });

  const t = T((r) => r.EventsView);

  return (
    <MainViewContainer loading={isLoading} error={error}>
      <h1>{t((r) => r.title)}</h1>
      <Table striped {...getTableProps()}>
        <thead>
          {headerGroups.map((headerGroup) => (
            <tr {...headerGroup.getHeaderGroupProps()}>
              {headerGroup.headers.map((column) => (
                <th {...column.getHeaderProps()}>{column.render("Header")}</th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody>
          {rows.map((row, i) => {
            prepareRow(row);
            return (
              <tr {...row.getRowProps()}>
                {row.cells.map((cell) => {
                  return (
                    <td {...cell.getCellProps()}>{cell.render("Cell")}</td>
                  );
                })}
              </tr>
            );
          })}
        </tbody>
      </Table>
    </MainViewContainer>
  );
}
