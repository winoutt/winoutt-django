import axios from 'axios'
import { replace } from 'voca'
import Alert from '../services/Alert'
import Progress from '../services/Progress'
import AuthToken from '../services/AuthToken'
import Router from '../services/Router'

export default {
  instance () {
    let headers =  {
      common: { 'X-Requested-With': 'XMLHttpRequest' }
    };
    if(typeof AuthToken.token() !== 'undefined'){
      headers.Authorization = `Token ${AuthToken.token()}`;
    }
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
    axios.defaults.xsrfCookieName = "csrftoken"
    return axios.create({
      baseURL: `${process.env.VUE_APP_URL}`,
      headers: headers
    })
  },

  errorHandler (error) {
    Progress.end()
    const data= error.response.data
    const status = error.response.status
    const isUnauthorized = status === 401
    const isLimitExceeded = status === 429
    const isNotFound = status === 404
    if (isUnauthorized) {
      Router.router.push({ name: 'SignIn' })
      Alert.error('Please sign in')
    } else if (isLimitExceeded || isNotFound) {
      return {}
    } else if (data) {
      const firstKey = Object.keys(data)[0];
      let message = ""
      if(typeof data[firstKey] === "object"){
        message = data[firstKey][0]
      }else{
        message = data[firstKey]
      }
      Alert.error(message);
    }
    return {}
  },

  async get (url, params) {
    try {
      Progress.start()
      const config = { params }
      const response = await this.instance().get(url, config)
      Progress.end()
      return response.data
    } catch (error) {
      return this.errorHandler(error)
    }
  },

  async post (url, data) {
    try {
      Progress.start()
      const response = await this.instance().post(url, data)
      Progress.end()
      return response.data
    } catch (error) {
      return this.errorHandler(error)
    }
  },

  async put (url, data) {
    try {
      Progress.start()
      const response = await this.instance().put(url, data)
      Progress.end()
      return response.data
    } catch (error) {
      return this.errorHandler(error)
    }
  },

  async patch (url, data) {
    try {
      Progress.start()
      const response = await this.instance().patch(url, data)
      Progress.end()
      return response.data
    } catch (error) {
      return this.errorHandler(error)
    }
  },

  async delete (url) {
    try {
      Progress.start()
      const response = await this.instance().delete(url)
      Progress.end()
      return response.data
    } catch (error) {
      return this.errorHandler(error)
    }
  },

  paginate (url) {
    const absoluteUrl = replace(url, `${process.env.MIX_APP_URL}/api`, '')
    return this.get(absoluteUrl)
  }
}
