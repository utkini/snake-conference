import {gamesList} from '../games_data'

const state = {
  gamesList: [],
  selectedGameId: null,

}

const mutations = {
  setGamesList: (state, gamesList) => state.gamesList = gamesList,
  resetGameList: (state) => state.gamesList = [],
  setSelectedGameId: (state, gameId) => state.selectedGameId = gameId,
  resetSelectedGameId: (state) => state.selectedGameId = null
}

const getters = {
  selectedGame: (state) => state.gamesList[state.selectedGameId],
  selectedPlayers: (state, getters) =>
    state.selectedGameId !== null ? Object.values(getters.selectedGame.players) : null,

}

const actions = {
  refreshGamesList({commit}) {
    commit('setGamesList', gamesList)
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}