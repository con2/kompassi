import * as React from 'react';
import { Translation } from 'react-i18next';
import Spinner from 'reactstrap/lib/Spinner';
import Table from 'reactstrap/lib/Table';

import Alert from 'reactstrap/lib/Alert';
import SessionContext from '../SessionContext';
import Session from '../SessionContext/Session';


interface DataTableProps {
  endpoint: string;
  columns: string[];
  ns?: string[];
}

interface DataTableState {
  loading: boolean;
  error?: string;
  items: any[];
}


export default class DataTable extends React.PureComponent<DataTableProps, DataTableState> {
  static contextType = SessionContext;
  context!: Session;

  defaultNamespace = 'DataTable';
  state: DataTableState = {
    loading: true,
    items: [],
  };

  componentDidMount() {
    this.getData();
  }

  async getData() {
    const { endpoint } = this.props;

    try {
      const items = await this.context.get(endpoint);
      this.setState({ items, loading: false });
    } catch(error) {
      this.setState({ error: error.message, loading: false });
    }

  }

  render() {
    const ns = this.props.ns ? this.props.ns.concat([this.defaultNamespace]) : [this.defaultNamespace];

    if (this.state.loading) {
      return <div style={{ textAlign: 'center', paddingTop: '1em' }}><Spinner /></div>;
    } else if (this.state.error) {
      return (
        <Translation ns={ns}>
          {(t) =>
            <Alert color="danger">{this.state.error}</Alert>
          }
        </Translation>
      );
    } else {
      const { columns } = this.props;
      const { items } = this.state;

      return (
        <Translation ns={ns}>
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
        </Translation>
      );
    }
    }
}
