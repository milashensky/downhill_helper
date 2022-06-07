const prepareBrackets = bracketContestants => {
  if (!Array.isArray(bracketContestants)) {
    return {};
  }
  const preparedBrackets = bracketContestants.reduce((brackets, bracketContestant) => {
    const result = { ...brackets };
    if (!result[bracketContestant.bracket_level]) {
      result[bracketContestant.bracket_level] = {};
    }
    if (!result[bracketContestant.bracket_level][bracketContestant.bracket_id]) {
      result[bracketContestant.bracket_level][bracketContestant.bracket_id] = [];
    }
    result[bracketContestant.bracket_level][bracketContestant.bracket_id].push(bracketContestant);
    return result;
  }, {});
  return preparedBrackets;
};


export default prepareBrackets;
