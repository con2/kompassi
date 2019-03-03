import * as React from 'react';

import DataTable from './DataTable';
import MainViewContainer from './MainViewContainer';


export default () => (
  <MainViewContainer>
    <h1>Forms</h1>
    <DataTable
      endpoint="forms"
      columns={['title', 'slug']}
      ns={['Form']}
    />
  </MainViewContainer>
);
