import React from 'react';
import { RouteComponentProps } from 'react-router';
import MainViewContainer from '../common/MainViewContainer';
import { T } from '../../translations';
import DataTable from '../common/DataTable';

const AccommodationOnboardingView: React.FC<RouteComponentProps<{ eventSlug: string }>> = ({ match }) => {
  const { eventSlug } = match.params;
  const t = T(r => r.AccommodationOnboardingView);

  return (
    <MainViewContainer>
      <h1>{t(r => r.title)}</h1>
      <DataTable
        endpoint={`events/${eventSlug}/accommodations`}
        columns={['surname', 'firstName', 'phoneNumber', 'status']}
        searchFields={['surname', 'firstName']}
        filterFields={['status']}
        standardActions={['open']}
      />
    </MainViewContainer>
  );
};

export default AccommodationOnboardingView;
