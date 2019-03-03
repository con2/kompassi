import * as React from 'react';

import { Translation } from 'react-i18next';

import MainViewContainer from './MainViewContainer';


export default () => (
  <Translation ns={['NotFound']}>
    {t => (
      <MainViewContainer>
        <h1>{t('notFoundHeader')}</h1>
        <p>{t('notFoundMessage')}</p>
      </MainViewContainer>
    )}
  </Translation>
);
