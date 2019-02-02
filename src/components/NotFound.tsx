import * as React from 'react';

import { NamespacesConsumer } from 'react-i18next';

import MainViewContainer from './MainViewContainer';


export default () => (
  <NamespacesConsumer ns={['NotFound']}>
    {t => (
      <MainViewContainer>
        <h1>{t('notFoundHeader')}</h1>
        <p>{t('notFoundMessage')}</p>
      </MainViewContainer>
    )}
  </NamespacesConsumer>
);
