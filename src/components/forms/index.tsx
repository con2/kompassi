import * as React from 'react';
import { Translation } from 'react-i18next';

import DataTable from '../common/DataTable';
import MainViewContainer from '../common/MainViewContainer';


const FormListView = () => (
  <Translation ns={['Forms']}>
    {t => (
      <MainViewContainer>
        <h1>{t('heading')}</h1>
        <DataTable
          endpoint="forms"
          columns={['title', 'slug']}
          ns={['Forms']}
        />
      </MainViewContainer>
    )}
  </Translation>
);

export default FormListView;
