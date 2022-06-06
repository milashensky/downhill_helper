const webpack = require('webpack');
const path = require('path');
const { defineConfig } = require('@vue/cli-service');


module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    allowedHosts: 'all',
  },
  configureWebpack: {
    resolve: {
      alias: {
        '@': path.join(__dirname, 'src'),
        'components': path.join(__dirname, 'src', 'components'),
        'utils': path.join(__dirname, 'src', 'utils'),
      },
    },
    plugins: [
      new webpack.DefinePlugin({
        'window.SENTRY_KEY': process.env.SENTRY_KEY,
      }),
      new webpack.DefinePlugin({
        'window.BACKEND_HOST': JSON.stringify(process.env.BACKEND_HOST || ''),
      }),
    ],
  },
});
