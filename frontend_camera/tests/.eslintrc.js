module.exports = {
  extends: [
    '../.eslintrc.js',
  ],
  plugins: ['jest'],
  rules: {
    'func-names': 'off', /* We wanna have anonymous functions in tests */
    'prefer-arrow-callback': 'off', /* We don't want eslint to warn us that we should prefer arrow callback for anonymous functions */
    'no-unused-expressions': 'off', /* Otherwise eslint complains about expect(...).to.be.true expressions */
    'global-require': 'off', /* We require tests based on if statements, therefore this is not necessary */
  },
  env: {
    'jest/globals': true,
  },
  settings: {
    'import/resolver': {
      alias: {
        map: [
          ['@', './src'],
          ['utils', './src/utils'],
          ['components', './src/components'],
          ['tests', './tests'],
        ],
        extensions: [
          '.js',
          '.json',
          '.vue',
        ],
      },
    },
  },
};
