import _ from "lodash";

import config from "./ConfigService";
import { getJSON, putJSON, postJSON, deleteJSON } from "../helpers/FetchHelper";
import { sumRequirements, sumAllocated } from "../helpers/RequirementHelper";

function enrichJobCategories(jobCategories) {
  jobCategories.forEach(enrichJobCategory);
  return jobCategories;
}

function enrichJobCategory(jobCategory) {
  jobCategory.paths = {
    detail: `/${jobCategory.slug}`,
  };
  jobCategory.urls = {
    detail: `${config.urls.base}/${jobCategory.slug}`,
  };

  if (jobCategory.people) {
    jobCategory.people.forEach((person) => {
      person.text = `${person.fullName} (${person.currentlyAssigned}/${person.totalWork})`;
    });
    jobCategory.peopleById = _.keyBy(jobCategory.people, "id");
  }

  if (jobCategory.jobs) {
    (jobCategory.allocated = sumAllocated(jobCategory.jobs)),
      (jobCategory.requirements = sumRequirements(jobCategory.jobs));
    jobCategory.jobs.forEach((job) => {
      job.jobCategory = jobCategory;
      job.shifts.forEach((shift) => {
        shift.job = job;
        shift.person = jobCategory.peopleById[shift.person];
      });
    });
  }

  return jobCategory;
}

export function getJobCategories() {
  return getJSON(config.urls.jobCategoryApi).then(enrichJobCategories);
}

export function getJobCategory(slug) {
  return getJSON(`${config.urls.jobCategoryApi}/${slug}`).then(
    enrichJobCategory,
  );
}

export function setRequirement(job, doc) {
  return postJSON(
    `${config.urls.jobCategoryApi}/${job.jobCategory.slug}/jobs/${job.slug}/requirements`,
    doc,
  ).then(enrichJobCategory);
}

export function createJob(jobCategory, newJob) {
  return postJSON(
    `${config.urls.jobCategoryApi}/${jobCategory.slug}/jobs`,
    newJob,
  ).then(enrichJobCategory);
}

export function updateJob(job, update) {
  const url = `${config.urls.jobCategoryApi}/${job.jobCategory.slug}/jobs/${job.slug}`;
  return putJSON(url, update).then(enrichJobCategory);
}

export function deleteJob(job) {
  const url = `${config.urls.jobCategoryApi}/${job.jobCategory.slug}/jobs/${job.slug}`;
  return deleteJSON(url).then(enrichJobCategory);
}

export function createShift(jobCategory, newShift) {
  return postJSON(
    `${config.urls.jobCategoryApi}/${jobCategory.slug}/shifts`,
    newShift,
  ).then(enrichJobCategory);
}

export function updateShift(shift, update) {
  const url = `${config.urls.jobCategoryApi}/${shift.job.jobCategory.slug}/shifts/${shift.id}`;
  return putJSON(url, update).then(enrichJobCategory);
}

export function deleteShift(shift) {
  const url = `${config.urls.jobCategoryApi}/${shift.job.jobCategory.slug}/shifts/${shift.id}`;
  return deleteJSON(url).then(enrichJobCategory);
}
