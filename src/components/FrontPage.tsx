import * as React from 'react';

import Alert from 'reactstrap/lib/Alert';

import DataTable from './DataTable';
import MainViewContainer from './MainViewContainer';


class EventTable extends DataTable {
  getHref(item: any) {
    return `/events/${super.getHref(item)}`;
  }
}


export default () => (
  <MainViewContainer>
    <Alert color="warning">This is by no means the final front page for Kompassi v2. Just a demo of the table component for now.</Alert>
    <h1>Events</h1>
    <EventTable
      endpoint="events"
      columns={['name', 'headline']}
      standardActions={['open']}
      ns={["Event"]}
    />
  </MainViewContainer>
);
