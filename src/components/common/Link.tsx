import React from 'react';
import { Link as RouterLink } from 'react-router-dom';

interface LinkProps {
  to: string;
}

const Link: React.FC<LinkProps> = ({ to, children }) =>
  to.includes('://') ? (
    <a href={to} target="_blank" rel="noopener noreferrer">
      {children}
    </a>
  ) : (
    <RouterLink to={to}>{children}</RouterLink>
  );

export default Link;
