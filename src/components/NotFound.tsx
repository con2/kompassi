import * as React from 'react';

import MainViewContainer from './common/MainViewContainer';
import { t } from '../translations';

const NotFound = () => (
  <MainViewContainer>
    <h1>{t(r => r.NotFound.notFoundHeader)}</h1>
    <p>{t(r => r.NotFound.notFoundMessage)}</p>
  </MainViewContainer>
);

export default NotFound;
