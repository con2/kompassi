import * as React from 'react';
import { NamespacesConsumer } from 'react-i18next';

import { UncontrolledDropdown } from 'reactstrap';
import Collapse from 'reactstrap/lib/Collapse';
import DropdownItem from 'reactstrap/lib/DropdownItem';
import DropdownMenu from 'reactstrap/lib/DropdownMenu';
import DropdownToggle from 'reactstrap/lib/DropdownToggle';
import Nav from 'reactstrap/lib/Nav';
import Navbar from 'reactstrap/lib/Navbar';
import NavbarBrand from 'reactstrap/lib/NavbarBrand';
import NavbarToggler from 'reactstrap/lib/NavbarToggler';
import NavItem from 'reactstrap/lib/NavItem';
import NavLink from 'reactstrap/lib/NavLink';

import { SessionConsumer } from '../SessionContext';

import './index.css';


interface NavigationState {
  isOpen: boolean;
}


export default class Navigation extends React.Component<{}, NavigationState> {
  constructor(props: {}) {
    super(props);

    this.state = {
      isOpen: false
    };
  }

  render() {
    return (
      <NamespacesConsumer ns={['Navigation']}>
        {t => (
          <SessionConsumer>
            {session => (
              <Navbar color="dark" dark={true} expand="md" id="kompassi-navbar">
                <NavbarBrand href="/">Kompassi <sup><small>v2 BETA</small></sup></NavbarBrand>
                <NavbarToggler onClick={this.toggle} />
                <Collapse isOpen={this.state.isOpen} navbar={true}>
                  <Nav className="ml-auto" navbar={true}>
                    {session.user ? (
                      // Logged in
                      <UncontrolledDropdown nav={true} inNavbar={true}>
                        <DropdownToggle nav={true} caret={true}>{session.user.displayName}</DropdownToggle>
                        <DropdownMenu right={true}>
                          <DropdownItem>
                            Option 1
                          </DropdownItem>
                          <DropdownItem>
                            Option 2
                          </DropdownItem>
                          <DropdownItem divider={true} />
                          <DropdownItem onClick={session.logOut}>{t('logOut')}</DropdownItem>
                        </DropdownMenu>
                      </UncontrolledDropdown>
                    ) : (
                      // Not logged in
                      <NavItem>
                        <NavLink onClick={session.logIn}>{t('logIn')}</NavLink>
                      </NavItem>
                    )}
                  </Nav>
                </Collapse>
              </Navbar>
            )}
          </SessionConsumer>
        )}
      </NamespacesConsumer>
    );
  }

  private toggle = () => {
    this.setState({
      isOpen: !this.state.isOpen
    });
  }
}
