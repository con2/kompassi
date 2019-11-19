import * as React from 'react';
import { LinkContainer } from 'react-router-bootstrap';
import Link from '../Link';

import Alert from 'reactstrap/lib/Alert';
import Button from 'reactstrap/lib/Button';
import ButtonGroup from 'reactstrap/lib/ButtonGroup';
import Table from 'reactstrap/lib/Table';

import Loading from '../Loading';
import SessionContext from '../SessionContext';
import Session from '../SessionContext/Session';
import { TranslationFunction, T } from '../../../translations';
import { InputGroup, Input } from 'reactstrap';

type StandardAction = 'create' | 'open' | 'delete';
type Column<ItemType> = Extract<keyof ItemType, string>;

// TODO figure out default props under typescript
interface DataTableProps<ItemType> {
  endpoint: string;
  columns: Column<ItemType>[];
  standardActions?: StandardAction[];
  linkColumns?: Array<number | Column<ItemType>>;
  identityAttribute?: Column<ItemType>;
  t?: TranslationFunction<any>;
  filterFields?: Column<ItemType>[];
  searchFields?: Column<ItemType>[];
  getHref?(item: ItemType): string;
}

interface DataTableState<ItemType> {
  loading: boolean;
  error?: string;
  items: ItemType[];
  visibleItems: ItemType[];
  searchTerm: string;
}

export default class DataTable<ItemType> extends React.PureComponent<DataTableProps<ItemType>, DataTableState<ItemType>> {
  static contextType = SessionContext;
  context!: Session;

  state: DataTableState<ItemType> = {
    loading: true,
    items: [],
    visibleItems: [],
    searchTerm: '',
  };

  componentDidMount() {
    this.getData();
  }

  async getData() {
    const { endpoint } = this.props;

    try {
      const items = await this.context.get(endpoint);
      this.setState({ items, loading: false });
      this.search('');
    } catch (error) {
      this.setState({ error: error.message, loading: false });
    }
  }

  render() {
    const standardActions = this.props.standardActions || ['create', 'delete', 'open'];
    const t = this.props.t || T(r => r.DataTable);
    const tc = T(r => r.Common);

    if (this.state.loading) {
      return <Loading />;
    } else if (this.state.error) {
      return <Alert color="danger">{this.state.error}</Alert>;
    } else {
      const { columns } = this.props;
      const { visibleItems, searchTerm } = this.state;
      const searchFields = this.props.searchFields || [];

      return (
        <div className="DataTable">
          <ButtonGroup className="mb-2 mr-auto">
            {standardActions.includes('create') ? (
              <LinkContainer to={this.getCreateLink()}>
                <Button size="sm" color="success">
                  {t(r => r.create)}…
                </Button>
              </LinkContainer>
            ) : null}
          </ButtonGroup>
          {searchFields.length ? (
            <InputGroup className="mb-2 ml-auto" style={{ width: '20em' }}>
              <Input placeholder={tc(r => r.search) + '…'} value={searchTerm} onChange={this.onChangeSearchTerm} />
            </InputGroup>
          ) : null}
          <Table>
            <thead>
              <tr>
                {columns.map(columnName => (
                  <th key={columnName} scope="column">
                    {t(r => r[columnName])}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {visibleItems.map(item => (
                <tr key={this.getSlug(item)}>
                  {columns.map((columnName, columnIndex) => (
                    <td key={columnName}>
                      {this.isLinkColumn(columnName, columnIndex) ? (
                        <Link to={this.getHref(item)}>{item[columnName]}</Link>
                      ) : (
                        item[columnName]
                      )}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </Table>
        </div>
      );
    }
  }

  protected isLinkColumn(columnName: string, columnIndex: number) {
    if (this.props.standardActions && !this.props.standardActions.includes('open')) {
      return false;
    }

    const linkColumns = this.props.linkColumns || [0];
    return ['*', columnName, columnIndex].some(item => (linkColumns as (number | string)[]).includes(item));
  }

  protected getSlug(item: ItemType) {
    const { identityAttribute } = this.props;

    let slug = '';
    if (identityAttribute) {
      slug = '' + item[identityAttribute];
    } else {
      // Default to "slug". It may not exist
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      slug = (item as any).slug;
    }

    if (!slug) {
      throw new Error('Empty or missing identity attribute on item. Unable to create link.');
    }

    return slug;
  }

  protected getHref(item: ItemType) {
    const { endpoint, getHref } = this.props;

    if (getHref) {
      return getHref(item);
    }

    const slug = this.getSlug(item);

    return `/${endpoint}/${slug}`;
  }

  protected getCreateLink() {
    const { endpoint } = this.props;
    return `/${endpoint}/new`;
  }

  protected onChangeSearchTerm = (event: React.FormEvent<HTMLInputElement>) => {
    const searchTerm = event.currentTarget.value;
    this.search(searchTerm);
  };

  protected search(searchTerm: string) {
    const { searchFields } = this.props;
    const { items } = this.state;

    let visibleItems = items;
    if (searchFields && searchFields.length && searchTerm) {
      visibleItems = items.filter(item =>
        searchFields.some(column => item[column] && ('' + item[column]).toLowerCase().includes(searchTerm.toLowerCase())),
      );
    }

    this.setState({ visibleItems, searchTerm });
  }
}
