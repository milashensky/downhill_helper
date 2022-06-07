import prepareBrackets from 'utils/prepare-brackets';
import bracketsResponse from 'tests/brackets-response';


describe('prepareBrackets', () => {
  it('null safe', () => {
    const result1 = prepareBrackets();
    expect(result1).toStrictEqual({});
    const result2 = prepareBrackets([]);
    expect(result2).toStrictEqual({});
    const result3 = prepareBrackets({});
    expect(result3).toStrictEqual({});
  });


  it('splits brackets on levels', () => {
    const brackets = prepareBrackets(bracketsResponse);
    expect(brackets).toStrictEqual({
      0: {
        20: [
          {
            id: 42,
            contestant_name: 'klava',
            helmet_number: 8,
            qualification_number: 10,
            position: 1,
            bracket_id: 20,
            bracket_level: 0,
          },
          {
            id: 39,
            contestant_name: 'pupa',
            helmet_number: 4,
            qualification_number: 7,
            position: 2,
            bracket_id: 20,
            bracket_level: 0,
          },
          {
            id: 36,
            contestant_name: 'oleg',
            helmet_number: 3,
            qualification_number: 4,
            position: 3,
            bracket_id: 20,
            bracket_level: 0,
          },
          {
            id: 33,
            contestant_name: 'vitya',
            helmet_number: 1,
            qualification_number: 1,
            position: 4,
            bracket_id: 20,
            bracket_level: 0,
          },
        ],
        21: [
          {
            id: 43,
            contestant_name: 'tima',
            helmet_number: 6,
            qualification_number: 11,
            position: 1,
            bracket_id: 21,
            bracket_level: 0,
          },
          {
            id: 40,
            contestant_name: 'lupa',
            helmet_number: 5,
            qualification_number: 8,
            position: 2,
            bracket_id: 21,
            bracket_level: 0,
          },
          {
            id: 37,
            contestant_name: 'Borya',
            helmet_number: 11,
            qualification_number: 5,
            position: 3,
            bracket_id: 21,
            bracket_level: 0,
          },
          {
            id: 34,
            contestant_name: 'dima',
            helmet_number: 7,
            qualification_number: 2,
            position: 4,
            bracket_id: 21,
            bracket_level: 0,
          },
        ],
        22: [
          {
            id: 41,
            contestant_name: 'stepka',
            helmet_number: 2,
            qualification_number: 9,
            position: 1,
            bracket_id: 22,
            bracket_level: 0,
          },
          {
            id: 38,
            contestant_name: 'Milash',
            helmet_number: 12,
            qualification_number: 6,
            position: 2,
            bracket_id: 22,
            bracket_level: 0,
          },
          {
            id: 35,
            contestant_name: 'grisha',
            helmet_number: 10,
            qualification_number: 3,
            position: 3,
            bracket_id: 22,
            bracket_level: 0,
          },
        ],
      },
      1: {
        25: [
          {
            id: 52,
            contestant_name: 'tima',
            helmet_number: 6,
            qualification_number: 11,
            position: 1,
            bracket_id: 25,
            bracket_level: 1,
          },
          {
            id: 51,
            contestant_name: 'pupa',
            helmet_number: 4,
            qualification_number: 7,
            position: 2,
            bracket_id: 25,
            bracket_level: 1,
          },
          {
            id: 50,
            contestant_name: 'klava',
            helmet_number: 8,
            qualification_number: 10,
            position: 3,
            bracket_id: 25,
            bracket_level: 1,
          },
        ],
        26: [
          {
            id: 55,
            contestant_name: 'Milash',
            helmet_number: 12,
            qualification_number: 6,
            position: 1,
            bracket_id: 26,
            bracket_level: 1,
          },
          {
            id: 54,
            contestant_name: 'stepka',
            helmet_number: 2,
            qualification_number: 9,
            position: 2,
            bracket_id: 26,
            bracket_level: 1,
          },
          {
            id: 53,
            contestant_name: 'lupa',
            helmet_number: 5,
            qualification_number: 8,
            position: 3,
            bracket_id: 26,
            bracket_level: 1,
          },
        ],
      },
      2: {
        27: [
          {
            id: 59,
            contestant_name: 'stepka',
            helmet_number: 2,
            qualification_number: 9,
            position: null,
            bracket_id: 27,
            bracket_level: 2,
          },
          {
            id: 58,
            contestant_name: 'Milash',
            helmet_number: 12,
            qualification_number: 6,
            position: null,
            bracket_id: 27,
            bracket_level: 2,
          },
          {
            id: 57,
            contestant_name: 'pupa',
            helmet_number: 4,
            qualification_number: 7,
            position: null,
            bracket_id: 27,
            bracket_level: 2,
          },
          {
            id: 56,
            contestant_name: 'tima',
            helmet_number: 6,
            qualification_number: 11,
            position: null,
            bracket_id: 27,
            bracket_level: 2,
          },
        ],
      },
    });
  });
});
