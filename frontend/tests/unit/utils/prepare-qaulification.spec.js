import prepareQaulification from 'utils/prepare-qaulification';
import qaulificationResponse from 'tests/qaulification-response';


describe('prepareQaulification', () => {
  it('null safe', () => {
    const result1 = prepareQaulification();
    expect(result1).toStrictEqual([[], 0]);
    const result2 = prepareQaulification([]);
    expect(result2).toStrictEqual([[], 0]);
    const result3 = prepareQaulification();
    expect(result3).toStrictEqual([[], 0]);
  });


  it('splits brackets on levels', () => {
    const [quali, maxAttempts] = prepareQaulification(qaulificationResponse);
    expect(maxAttempts).toStrictEqual(2);
    expect(quali).toStrictEqual(
      [{
        id: 11,
        contestant_id: 11,
        contestant_name: 'vitya',
        qualification_time: 200.0,
        bestTime: 8.679,
        times: {
          11: 200.0,
          12: 8.679,
        },
        helmet_number: 20,
      }, {
        id: 2,
        contestant_id: 2,
        contestant_name: 'Borya',
        qualification_time: 59.998,
        bestTime: 59.998,
        times: { 2: 59.998 },
        helmet_number: 11,
      }, {
        id: 1,
        contestant_id: 1,
        contestant_name: 'Milash',
        qualification_time: 60.0,
        bestTime: 60.0,
        times: { 1: 60.0 },
        helmet_number: 12,
      }],
    );
  });
});
