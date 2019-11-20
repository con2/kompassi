import React from 'react';
import { useParams } from 'react-router-dom';
import useSWR from 'swr';

import Button from 'reactstrap/lib/Button';
import ButtonGroup from 'reactstrap/lib/ButtonGroup';

import MainViewContainer from '../common/MainViewContainer';
import SessionContext from '../common/SessionContext';

import SchemaForm from './SchemaForm';
import { T } from '../../translations';
import { Form } from './SchemaForm/models';

const FormView: React.FC<{}> = () => {
  const { slug } = useParams();
  const context = React.useContext(SessionContext);
  const { error, data } = useSWR<Form>(`forms/${slug}`, context.get);
  const t = T(r => r.Common);

  if (error || !data) {
    return <MainViewContainer error={error} loading={!data} />;
  }

  const { title, layout, fields } = data;

  return (
    <MainViewContainer>
      {title ? <h1>{title}</h1> : null}
      <SchemaForm fields={fields} layout={layout}>
        <ButtonGroup className="pt-3">
          <Button color="primary">{t(r => r.submit)}</Button>
        </ButtonGroup>
      </SchemaForm>
    </MainViewContainer>
  );
};

export default FormView;
