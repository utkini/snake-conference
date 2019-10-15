import axios from 'axios'
import config from 'config'

export class API{
  constructor(){}

  getGames() {
    const url = `${config.API_URL}/api/log/`;
    return axios.get(url).then(response => response.data);
  }

  getGame(gameId) {
    const url = `${config.API_URL}/api/log/${gameId}`;
    return axios.get(url).then(response => response.data);
  }
}
