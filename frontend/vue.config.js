module.exports = {
    publicPath: "http://127.0.0.1:8000/static/single_page/",
    outputDir: '../backend/project/single_page/static/single_page/',
    lintOnSave: process.env.NODE_ENV !== 'production',

    runtimeCompiler: true,
    
    chainWebpack: config => {
        config.output
            .filename('js/[name].js')
            .chunkFilename('js/[name].js')

        config.optimization
            .splitChunks(false)

        config.resolve.alias
            .set('__STATIC__', 'static')

        config.devServer
            .public('http://127.0.0.1:8000/static/single_page/')
            .host('127.0.0.1')
            .port(8080)
            .hotOnly(true)
            .watchOptions({poll: 1000})
            .https(false)
            .headers({"Access-Control-Allow-Origin": ["\*"]})
    }
};