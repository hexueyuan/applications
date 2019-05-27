import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

const state = {
    nickName: '',
    qqNumber: '',
    count: 0
}

const getters = {
    nickName(state) {
        return state.nickName
    },
    qqNumber(state) {
        return state.qqNumber
    },
    count(state) {
        return state.count
    }
}

const mutations = {
    setNickName(state, name) {
        state.nickName = name
    },
    setQQNumber(state, qq) {
        state.qqNumber = qq
    },
    setCount(state, count) {
        state.count = count
    }
}

const store = new Vuex.Store({
    state,
    getters,
    mutations
});
 
export default store;
