import React from 'react';

import Nav from 'reactstrap/lib/Nav';
import NavItem from 'reactstrap/lib/NavItem';
import NavLink from 'reactstrap/lib/NavLink';
import { TranslationFunction } from '../../translations';

interface TabsProps {
  children: { [tabName: string]: React.ReactNode };
  t?: TranslationFunction<any>;
}

interface TabsState {
  activeTab: string;
}

export default class Tabs extends React.Component<TabsProps, TabsState> {
  state: TabsState = {
    activeTab: '',
  };

  render() {
    const { children } = this.props;
    const t = this.props.t || (r => undefined);
    const activeTab = this.state.activeTab || Object.keys(children)[0];

    return (
      <>
        <Nav tabs={true} className="mb-2">
          {Object.keys(children).map(tab => (
            <NavItem key={tab}>
              <NavLink href="#" onClick={() => this.setState({ activeTab: tab })} active={activeTab === tab}>
                {t(r => r[tab]) || tab}
              </NavLink>
            </NavItem>
          ))}
        </Nav>

        {Object.entries(children).map(([tabName, tabContents]) => (
          <div key={tabName} style={{ display: activeTab === tabName ? '' : 'none' }}>
            {tabContents}
          </div>
        ))}
      </>
    );
  }
}
