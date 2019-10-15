const path = require('path')

module.exports = {
  publicPath: './',
  configureWebpack: {
    resolve: {
      modules: [
        path.resolve(__dirname, 'src')
      ]
    }
  }
}
