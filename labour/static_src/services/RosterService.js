import _ from 'lodash';

import config from './ConfigService';


function getJSON(url) {
  return fetch(url, {credentials: 'include'}).then(response => response.json());
}


function postJSON(url, body) {
  return fetch(url, {
    method: 'post',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  }).then(response => response.json());
}


function enrichJobCategories(jobCategories) {
  jobCategories.forEach(enrichJobCategory);
  return jobCategories;
}


function enrichJobCategory(jobCategory) {
  jobCategory.urls = {
    detail: `${config.urls.base}/${jobCategory.slug}`
  };

  if(jobCategory.jobs) {
    jobCategory.requirements = _.zip.apply(_, _.pluck(jobCategory.jobs, 'requirements')).map(_.sum);
    jobCategory.jobs.forEach(job => {
      job.jobCategory = jobCategory;
      job.requirementCells = requirementsToCells(job.requirements);
    });
  }

  jobCategory.requirementCells = requirementsToCells(jobCategory.requirements);

  return jobCategory;
}


function requirementsToCells(requirements) {
  return _.chain(config.workHours)
  .zip(requirements)
  .map(([hour, numPeopleRequired]) => ({
    hour: hour,
    allocated: 0, // TODO
    required: numPeopleRequired || 0, // XXX || 0 is for early devt
  })).value();
}


export function getJobCategories() {
  return getJSON(config.urls.jobCategoryApi).then(enrichJobCategories);
}


export function getJobCategory(slug) {
  return getJSON(`${config.urls.jobCategoryApi}/${slug}`).then(enrichJobCategory);
}


export function saveJobCategory(newJobCategory) {
  return getJobCategory(newJobCategory.slug).then(oldJobCategory => { _.extend(oldJobCategory, newJobCategory)});
}
