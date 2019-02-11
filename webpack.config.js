const path = require('path');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CleanWebpackPlugin = require('clean-webpack-plugin');
const autoprefixer = require('autoprefixer');

const outputDirectory = path.resolve(__dirname, 'therewasanattempt/static/therewasanattempt');

module.exports = {
  mode: 'development',
  entry: [
    './static/scss/bootstrap-custom.scss',
    './static/images/contoso-logo.png',
    './static/images/banner.jpg',
  ],
  output: {
    path: outputDirectory,
    filename: 'js/main.js'
  },
  plugins: [
    new CleanWebpackPlugin([outputDirectory]),
    new MiniCssExtractPlugin({
      filename: "css/[name].css",
      chunkFilename: "css/[name].css"
    }),
  ],
  module: {
    rules: [
      {
        test: /\.(woff|woff2|eot|ttf|svg)$/i,
        use: {
          loader: 'file-loader',
          options: {
            name: '[name].[ext]',
            publicPath: '../fonts',
            outputPath: 'fonts'
          }
        }
      },
      {
        test: /\.(jpg|png|gif)$/i,
        use: {
          loader: 'file-loader',
          options: {
            name: '[name].[ext]',
            outputPath: 'images'
          }
        }
      },
      {
        test: /\.(scss)$/,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader',
          { loader: 'postcss-loader', options: { ident: 'postcss', plugins: [ autoprefixer() ] } },
          'sass-loader'
        ],
      }
    ]
  }
};
