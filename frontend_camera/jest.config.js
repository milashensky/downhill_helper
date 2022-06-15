module.exports = {
  preset: '@vue/cli-plugin-unit-jest',
  moduleFileExtensions: [
    'js',
    'json',
    'vue',
  ],
  moduleNameMapper: {
    '@/(.*)$': '<rootDir>/src/$1',
    'tests/(.*)$': '<rootDir>/tests/$1',
    'utils/(.*)$': '<rootDir>/src/utils/$1',
    'components/(.*)$': '<rootDir>/src/components/$1',
  },
  testMatch: [
    '**/__tests__/*.{j,t}s?(x)',
    '**/tests/unit/**/*.spec.{j,t}s?(x)',
    '**/tests/integration/**/*.test.{j,t}s?(x)',
  ],
};
