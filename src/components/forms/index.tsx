import * as React from 'react';

import DataTable from '../common/DataTable';
import MainViewContainer from '../common/MainViewContainer';
import { t, T } from '../../translations';

const FormListView = () => (
  <MainViewContainer>
    <h1>{t(r => r.Forms.heading)}</h1>
    <DataTable
      endpoint="forms"
      columns={['title', 'slug']}
      t={T(r => r.Forms)}
      standardActions={['create', 'open', 'edit', 'delete']}
    />
  </MainViewContainer>
);

export default FormListView;
