module.exports = {
  'root': true,
  'env': {
    node: true,
  },
  'extends': [
    'plugin:vue/vue3-essential',
    '@vue/airbnb',
  ],
  'parserOptions': {
    parser: '@babel/eslint-parser',
  },
  'rules': {
    'indent': [
      'error',
      2,
    ],
    'no-alert': 0,
    'radix': ['error', 'as-needed'],
    'arrow-parens': [
      'error',
      'as-needed',
    ],
    'max-len': [
      'error',
      {
        'code': 380,
      },
    ],
    'import/newline-after-import': [
      'error',
      {
        'count': 2,
      },
    ],
    'no-console': ['warn', { 'allow': ['warn', 'error'] }],
    'vuejs-accessibility/click-events-have-key-events': 0,
    'no-multiple-empty-lines': [
      'error',
      {
        'max': 2,
        'maxEOF': 0,
      },
    ],
    'import/extensions': [
      'error',
      'never',
    ],
    'brace-style': [
      'error',
      'stroustrup',
    ],
    'quotes': ['error', 'single'],
    'quote-props': ['error', 'consistent'],
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
  },
};
