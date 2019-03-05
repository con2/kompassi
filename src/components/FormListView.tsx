import * as React from 'react';
import { Translation } from 'react-i18next';

import DataTable from './DataTable';
import MainViewContainer from './MainViewContainer';


export default () => (
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
