import * as React from 'react';

import { Translation } from 'react-i18next';

import MainViewContainer from './common/MainViewContainer';


const NotFound = () => (
  <Translation ns={['NotFound']}>
    {t => (
      <MainViewContainer>
        <h1>{t('notFoundHeader')}</h1>
        <p>{t('notFoundMessage')}</p>
      </MainViewContainer>
    )}
  </Translation>
);

export default NotFound;
