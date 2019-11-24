import * as React from 'react';

import DataTable from '../common/DataTable';
import MainViewContainer from '../common/MainViewContainer';
import { t, T } from '../../translations';
import { useParams } from 'react-router';

interface Params {
  slug: string;
}

const FormResponsesView: React.FC<{}> = () => {
  const { slug } = useParams<Params>();

  return (
    <MainViewContainer loading={!slug}>
      <h1>{t(r => r.FormResponses.heading)}</h1>
      <DataTable endpoint={`forms/${slug}/responses`} columns={['title', 'slug']} t={T(r => r.Forms)} />
    </MainViewContainer>
  );
};

export default FormResponsesView;
