// import {gamesList} from '../games_data'
import {API} from '../../api'


const api = new API();


const state = {
  gamesList: [],
  selectedGameId: null,
  selectedGame: null,
}

const mutations = {
  setGamesList: (state, gamesList) => state.gamesList = gamesList,
  resetGameList: (state) => state.gamesList = [],
  setSelectedGame: (state, game) => state.selectedGame = game,
  resetSelectedGame: (state) => state.selectedGame = null,
  setSelectedGameId: (state, gameId) => state.selectedGameId = gameId,
  resetSelectedGameId: (state) => state.selectedGameId = null,
}

const getters = {
  selectedPlayers: (state) =>
    state.selectedGame !== null ? Object.values(state.selectedGame.players) : null,

}

const actions = {
  async refreshGamesList({commit}) {
    let gamesList = await api.getGames();
    commit('setGamesList', gamesList)
  },

  async getGame({commit}, gameId) {
    let game = await api.getGame(gameId);
    commit('setSelectedGame', game)
    commit('setSelectedGameId', gameId)
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
