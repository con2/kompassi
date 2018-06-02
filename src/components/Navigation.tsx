import * as React from 'react';
import {
    Collapse,
    DropdownItem,
    DropdownMenu,
    DropdownToggle,
    Nav,
    Navbar,
    NavbarBrand,
    NavbarToggler,
    UncontrolledDropdown,
} from 'reactstrap';

import './Navigation.css';



interface IState {
    isOpen: boolean;
}


export default class Example extends React.Component<{}, IState> {
    constructor(props: {}) {
        super(props);

        this.toggle = this.toggle.bind(this);
        this.state = {
            isOpen: false
        };
    }

    public render() {
        return (
            <div>
                <Navbar color="dark" dark={true} expand="md" id="kompassi-navbar">
                    <NavbarBrand href="/">Kompassi <sup><small>v2 BETA</small></sup></NavbarBrand>
                    <NavbarToggler onClick={this.toggle} />
                    <Collapse isOpen={this.state.isOpen} navbar={true}>
                        <Nav className="ml-auto" navbar={true}>
                            <UncontrolledDropdown nav={true} inNavbar={true}>
                                <DropdownToggle nav={true} caret={true}>
                                    Santtu Pajukanta
                                </DropdownToggle>
                                <DropdownMenu right={true}>
                                    <DropdownItem>
                                        Option 1
                                    </DropdownItem>
                                    <DropdownItem>
                                        Option 2
                                    </DropdownItem>
                                    <DropdownItem divider={true} />
                                    <DropdownItem>
                                        Kirjaudu ulos
                                    </DropdownItem>
                                </DropdownMenu>
                            </UncontrolledDropdown>
                        </Nav>
                    </Collapse>
                </Navbar>
            </div>
        );
    }

    private toggle() {
        this.setState({
            isOpen: !this.state.isOpen
        });
    }
}
