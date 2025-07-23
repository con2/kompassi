import Cookies from "js-cookie";

const csrfToken = Cookies.get("csrftoken");

export function getJSON(url) {
  return fetch(url, { credentials: "include" }).then((response) =>
    response.json(),
  );
}

function thrustJSON(method, url, body) {
  return fetch(url, {
    method: method,
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify(body),
    credentials: "include",
  }).then((response) => response.json());
}

export function postJSON(url, body) {
  return thrustJSON("post", url, body);
}

export function putJSON(url, body) {
  return thrustJSON("put", url, body);
}

export function deleteJSON(url, body) {
  return fetch(url, {
    method: "delete",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    credentials: "include",
  }).then((response) => response.json());
}
