import _ from 'lodash';

import config from './ConfigService';
import {getJSON, putJSON, postJSON, deleteJSON} from '../helpers/FetchHelper';
import {sumRequirements} from '../helpers/RequirementHelper';


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
    jobCategory.requirements = sumRequirements(jobCategory.jobs);
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


export function createJob(jobCategory, newJob) {
  return postJSON(`${config.urls.jobCategoryApi}/${jobCategory.slug}/jobs`, newJob)
  .then(enrichJobCategory);
}


export function updateJob(job, update) {
  const url = `${config.urls.jobCategoryApi}/${job.jobCategory.slug}/jobs/${job.slug}`;
  return putJSON(url, update).then(enrichJobCategory);
}


export function deleteJob(job) {
  const url = `${config.urls.jobCategoryApi}/${job.jobCategory.slug}/jobs/${job.slug}`;
  return deleteJSON(url).then(enrichJobCategory);
}
