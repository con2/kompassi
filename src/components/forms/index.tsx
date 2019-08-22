import * as React from 'react';

import DataTable from '../common/DataTable';
import MainViewContainer from '../common/MainViewContainer';
import { t } from '../../translations';

const FormListView = () => (
  <MainViewContainer>
    <h1>{t(r => r.Forms.heading)}</h1>
    <DataTable endpoint="forms" columns={['title', 'slug']} ns={['Forms']} />
  </MainViewContainer>
);

export default FormListView;
