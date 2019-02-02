import * as React from 'react';
import { NamespacesConsumer } from 'react-i18next';
import Spinner from 'reactstrap/lib/Spinner';
import Table from 'reactstrap/lib/Table';

import SessionContext from '../SessionContext';
import Session from '../SessionContext/Session';


interface DataTableProps {
  endpoint: string;
  columns: string[];
  ns?: string[];
}

interface DataTableState<ItemType> {
  loading: boolean;
  items: ItemType[];
}


export default class DataTable<ItemType> extends React.PureComponent<DataTableProps, DataTableState<ItemType>> {
  static contextType = SessionContext;
  context!: Session;

  defaultNamespace = 'DataTable';
  state = {
    loading: true,
    items: [],
  };

  async componentDidMount() {
    const items = await this.context.get('events');
    this.setState({ items, loading: false });
  }

  render() {
    if (this.state.loading) {
      return <div style={{ textAlign: 'center', paddingTop: '1em' }}><Spinner /></div>;
    }

    const { columns } = this.props;
    const { items } = this.state;
    const ns = this.props.ns ? this.props.ns.concat([this.defaultNamespace]) : [this.defaultNamespace];

    return (
      <NamespacesConsumer ns={ns}>
        {(t) => (
          <Table>
            <thead>
              <tr>
                {columns.map(columnName => (
                  <th key={columnName}>{t(columnName)}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {items.map((item, index) => (
                <tr key={index}>
                  {columns.map(columnName => (
                    <td key={columnName}>{item[columnName]}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </Table>
        )}
      </NamespacesConsumer>
    );
  }
}
