import React from 'react';

import Nav from 'reactstrap/lib/Nav';
import NavItem from 'reactstrap/lib/NavItem';
import NavLink from 'reactstrap/lib/NavLink';
import { TranslationFunction } from '../../translations';

interface TabsProps<T extends { [tabName: string]: React.ReactNode }> {
  children: T;
  t?: TranslationFunction<any>;
  activeTab?: string;
  onChange?(tab: keyof T): void;
}

function Tabs<T extends { [tabName: string]: React.ReactNode }>(props: TabsProps<T>) {
  const { children } = props;
  const t = props.t || (r => '');
  const activeTab = props.activeTab || Object.keys(children)[0];
  const onChange = props.onChange || (() => {});

  const onClick = React.useCallback((tab: keyof T) => () => onChange(tab), [onChange]);

  return (
    <>
      <Nav tabs={true} className="mb-2">
        {Object.keys(children).map(tab => (
          <NavItem key={tab}>
            <NavLink href="#" onClick={onClick(tab as keyof T)} active={activeTab === tab}>
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

export default Tabs;
