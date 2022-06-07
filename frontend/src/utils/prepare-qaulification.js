const prepareQaulification = contestantQualifications => {
  if (!Array.isArray(contestantQualifications)) {
    return [[], 0];
  }
  let maxAttempts = 0;
  const qualificationTimesByContestant = contestantQualifications.reduce((qualifications, contestantQualification) => {
    const {
      contestant_id: contestantId,
      qualification_time: qualificationTime,
    } = contestantQualification;
    const result = {
      [contestantId]: {
        ...contestantQualification,
        times: {},
      },
      ...qualifications,
    };
    result[contestantId].times[contestantQualification.id] = qualificationTime;
    const attempts = Object.values(result[contestantId].times).length;
    if (attempts > maxAttempts) {
      maxAttempts = attempts;
    }
    [result[contestantId].bestTime] = Object.values(result[contestantId].times).sort((a, b) => a - b);
    return result;
  }, {});
  const qualification = Object.values(qualificationTimesByContestant).sort((a, b) => a.bestTime - b.bestTime);
  return [qualification, maxAttempts];
};


export default prepareQaulification;
