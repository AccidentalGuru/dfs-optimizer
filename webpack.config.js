// require our dependencies
var path = require('path')
var webpack = require('webpack')

module.exports = {
  // the base directory (absolute path) for resolving the entry option
  context: __dirname,
  // the entry point of the react application
  entry: './app/static/js/index',
  output: {
    // where you want your compiled bundle to be stored
    path: path.resolve('./app/static/'),
    filename: 'bundle.js',
  },
  plugins: [
    // makes jQuery available in every module
    new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery',
            'window.jQuery': 'jquery'
        })
  ],
  module: {
    rules: [
      {
        test: /\.jsx?/,
        // we don't want babel to transpile files in node_modules. would take a long time
        exclude: /node_modules/,
        loader: 'babel-loader',
        query: {
          //specify that we will be dealing with React code
          presets: ['react']
        }
      },
      {
        test:/\.css$/,
        use:['css-loader']
      }
    ]
  },
  resolve: {
       //tells webpack where to look for modules
       //modulesDirectories: ['node_modules'],

       //extensions that should be used to resolve modules
       extensions: ['.js', '.jsx', '.css']
   }
}
