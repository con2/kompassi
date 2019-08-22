import * as React from 'react';

import Alert from 'reactstrap/lib/Alert';

import DataTable from './common/DataTable';
import MainViewContainer from './common/MainViewContainer';
import { T } from '../translations';
import Config from '../Config';

interface Event {
  slug: string;
  name: string;
  headline: string;
}
class EventTable extends DataTable<Event> {}

export default () => {
  const t = T(r => r.Event);

  return (
    <MainViewContainer>
      <Alert color="warning">{t(r => r.workInProgress)}</Alert>
      <h1>{t(r => r.title)}</h1>
      <EventTable
        endpoint="events"
        columns={['name', 'headline']}
        standardActions={['open']}
        searchFields={['name']}
        t={t}
        getHref={event => `${Config.api.baseUrl}/events/${event.slug}`}
      />
    </MainViewContainer>
  );
};
