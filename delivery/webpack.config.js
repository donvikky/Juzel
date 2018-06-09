const path = require('path')

module.exports = {
    entry:{
        app: path.join(__dirname, 'src', 'app.js'),
        menu: path.join(__dirname, 'src', 'menu.js'),
    },
    output:{
        path: path.resolve(__dirname, 'static','js'),
        filename: '[name].bundle.js'
    },
    module:{
        rules: [
            {
              test: /\.js$/,
              exclude: /node_modules/,
              use: {
                loader: "babel-loader"
              }
            }
        ]
    },
    resolve: {
        alias: {
          'vue$': 'vue/dist/vue.esm.js' // 'vue/dist/vue.common.js' for webpack 1
        }
    }
}