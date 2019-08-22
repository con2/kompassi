import ClientOAuth2 from 'client-oauth2';

import Config from '../../../Config';

export type Method = 'GET' | 'POST' | 'PUT' | 'DELETE';

export async function fetchWithCredentials(method: Method, path: string, token: string, data?: any) {
  const url = `${Config.api.baseUrl}/api/v3/${path}`;
  const headers: { [name: string]: string } = {
    accept: 'application/json',
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const init: RequestInit = { headers, method };

  if (data) {
    headers['Content-Type'] = 'application/json';
    init.body = JSON.stringify(data);
  }

  const response = await fetch(url, init);

  if (!response.ok) {
    throw new Error(response.statusText);
  }

  return response.json();
}

function getPath() {
  if (window.location.search) {
    return `${window.location.pathname}?${window.location.search}`;
  } else {
    return window.location.pathname;
  }
}

function encodeQuery(query: { [key: string]: string }) {
  const params = new URLSearchParams();
  Object.entries(query).forEach(([key, value]) => params.set(key, value));
  return params.toString();
}

export function getOAuth2() {
  const query = encodeQuery({ next: getPath() });

  return new ClientOAuth2({
    clientId: Config.api.clientId,
    accessTokenUri: `${Config.api.baseUrl}/oauth2/token`,
    authorizationUri: `${Config.api.baseUrl}/oauth2/authorize`,
    redirectUri: `${Config.publicUrl}/oauth2/callback?${query}`,
    scopes: ['read', 'write'],
  });
}
