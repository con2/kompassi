import * as React from 'react';
import { Translation } from 'react-i18next';
import { LinkContainer } from 'react-router-bootstrap';
import { Link } from 'react-router-dom';

import Alert from 'reactstrap/lib/Alert';
import Button from 'reactstrap/lib/Button';
import ButtonGroup from 'reactstrap/lib/ButtonGroup';
import Spinner from 'reactstrap/lib/Spinner';
import Table from 'reactstrap/lib/Table';

import SessionContext from '../SessionContext';
import Session from '../SessionContext/Session';


type StandardAction = 'create' | 'open' | 'delete';


// TODO figure out default props under typescript
interface DataTableProps {
  endpoint: string;
  columns: string[];
  standardActions?: StandardAction[];
  linkColumns?: Array<number | string>;
  identityAttribute?: string;
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
    } catch (error) {
      this.setState({ error: error.message, loading: false });
    }

  }

  render() {
    const ns = this.props.ns ? this.props.ns.concat([this.defaultNamespace]) : [this.defaultNamespace];
    const standardActions = this.props.standardActions || ['create', 'delete', 'open'];

    if (this.state.loading) {
      return <div style={{ textAlign: 'center', paddingTop: '1em' }}><Spinner /></div>;
    } else if (this.state.error) {
      return <Alert color="danger">{this.state.error}</Alert>;
    } else {
      const { columns } = this.props;
      const { items } = this.state;

      return (
        <Translation ns={ns}>
          {(t) => (
            <div className="DataTable">
              <ButtonGroup className="mb-2">
                {standardActions.includes('create') ? (
                  <LinkContainer to={this.getCreateLink()}>
                    <Button size="sm" color="success">{t('create')}…</Button>
                  </LinkContainer>
                ) : null}
              </ButtonGroup>
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
                      {columns.map((columnName, columnIndex) => (
                        <td key={columnName}>
                          {this.isLinkColumn(columnName, columnIndex) ? (
                            <Link to={this.getHref(item)}>{item[columnName]}</Link>
                          ) : item[columnName]}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </Table>
            </div>
          )}
        </Translation>
      );
    }
  }

  protected isLinkColumn(columnName: string, columnIndex: number) {
    if (this.props.standardActions && !this.props.standardActions.includes('open')) {
      return false;
    }

    const linkColumns = this.props.linkColumns || [0];
    return ['*', columnName, columnIndex].some(item => linkColumns.includes(item));
  }

  protected getHref(item: any) {
    const { endpoint, identityAttribute } = this.props;
    const slug = item[identityAttribute || 'slug'];
    return `/${endpoint}/${slug}`;
  }

  protected getCreateLink() {
    const { endpoint } = this.props;
    return `/${endpoint}/new`;
  }
}
