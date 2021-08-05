import Http from './Http'

export default {
  create (data) {
    return Http.post('reports/api/reportings', data)
  }
}
