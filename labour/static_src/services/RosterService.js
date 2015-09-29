import _ from 'lodash';

import Cookies from 'js-cookie';

import config from './ConfigService';

const csrfToken = Cookies.get('csrftoken');


function getJSON(url) {
  return fetch(url, {credentials: 'include'}).then(response => response.json());
}


function postJSON(url, body) {
  return fetch(url, {
    method: 'post',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken,
    },
    body: JSON.stringify(body),
    credentials: 'include',
  }).then(response => response.json());
}


function enrichJobCategories(jobCategories) {
  jobCategories.forEach(enrichJobCategory);
  return jobCategories;
}


function enrichJobCategory(jobCategory) {
  jobCategory.paths = {
    detail: `/${jobCategory.slug}`
  };
  jobCategory.urls = {
    detail: `${config.urls.base}/${jobCategory.slug}`
  };

  if(jobCategory.jobs) {
    jobCategory.requirements = _.zip.apply(_, _.pluck(jobCategory.jobs, 'requirements')).map(_.sum);
    jobCategory.jobs.forEach(job => { job.jobCategory = jobCategory; });
  }

  return jobCategory;
}

export function getJobCategories() {
  return getJSON(config.urls.jobCategoryApi).then(enrichJobCategories);
}


export function getJobCategory(slug) {
  return getJSON(`${config.urls.jobCategoryApi}/${slug}`).then(enrichJobCategory);
}


export function setRequirement(job, doc) {
  return postJSON(`${config.urls.jobCategoryApi}/${job.jobCategory.slug}/jobs/${job.slug}/requirements`, doc)
  .then(enrichJobCategory);
}
