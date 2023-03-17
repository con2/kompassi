import useSWR from "swr";
import { useTable, Column } from "react-table";

import MainViewContainer from "./common/MainViewContainer";
import { Table } from "react-bootstrap";

const fetcher = (url: string) => fetch(url).then((res) => res.json());

interface Event {
  url: string;
  slug: string;
  name: string;
  startTime: string;
  endTime: string;
  headline: string;
  homepageUrl: string;
}

const columns: Column<Event>[] = [
  {
    Header: "Name",
    accessor: "name",
    Cell: ({ row, value }) => <a href={row.original.url}>{value}</a>,
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

  return (
    <MainViewContainer loading={isLoading} error={error}>
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
