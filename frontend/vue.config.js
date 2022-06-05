const webpack = require('webpack');
const path = require('path');
const { defineConfig } = require('@vue/cli-service');


module.exports = defineConfig({
  transpileDependencies: true,
  configureWebpack: {
    resolve: {
      alias: {
        '@': path.join(__dirname, 'src'),
        'pages': path.join(__dirname, 'src', 'pages'),
        'components': path.join(__dirname, 'src', 'components'),
        'mixins': path.join(__dirname, 'src', 'mixins'),
      },
    },
    plugins: [
      new webpack.DefinePlugin({
        'window.SENTRY_KEY': process.env.SENTRY_KEY,
      }),
    ],
  },
});
