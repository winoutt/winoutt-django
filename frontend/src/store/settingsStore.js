import { isEqual } from 'lodash'
import UserState from '../State/UserState'

export default {
  namespaced: true,
  state: {
    active: 'profile',
    settings: {
      is_dark_mode: false,
      enabled_notification: false
    },
    user: {
      first_name: '',
      last_name: '',
      username: '',
      email: '',
      bio: '',
      website: {
        company: '',
        personal: ''
      },
      date_of_birth: '',
      gender: '',
      city: '',
      country: '',
      avatar: '',
      title: '',
      sessionAt: ''
    },
    customTitle: ''
  },

  mutations: {
    replaceActive (state, active) {
      state.active = active
    },
    replaceSettings (state, settings) {
      state.settings = settings
    },
    replaceUser (state, user) {
      state.user = user
    },
    replaceFirstName (state, firstName) {
      state.user.first_name = firstName
    },
    replaceLastName (state, lastName) {
      state.user.last_name = lastName
    },
    replaceUserName (state, username) {
      state.user.username = username
    },
    replaceEmail (state, email) {
      state.user.email = email
    },
    replaceBio (state, bio) {
      state.user.end_user.bio = bio
    },
    replaceCompanyWebsite (state, companyWebsite) {
      state.user.website.company = companyWebsite
    },
    replacePersonalWebsite (state, personalWebsite) {
      state.user.website.personal = personalWebsite
    },
    replaceDateOfBirth (state, dateOfBirth) {
      state.user.end_user.date_of_birth = dateOfBirth
    },
    replaceGender (state, gender) {
      state.user.end_user.gender = gender
    },
    replaceCity (state, city) {
      state.user.end_user.city = city
    },
    replaceCountry (state, country) {
      state.user.end_user.country = country
    },
    replaceAvatar (state, avatar) {
      state.user.avatar = avatar
    },
    replaceTitle (state, title) {
      state.user.end_user.title = title
    },
    replaceCustomTitle (state, customTitle) {
      state.customTitle = customTitle
    },
    replaceDarkMode (state, isDarkMode) {
      state.settings.is_dark_mode = isDarkMode
    },
    replaceEnableNotification (state, isEnabled) {
      state.settings.enabled_notification = isEnabled
    }
  },

  getters: {
    active: state => state.active,
    settings: state => state.settings,
    user: state => state.user,
    firstName: state => state.user.first_name,
    lastName: state => state.user.last_name,
    email: state => state.user.email,
    username: state => state.user.username,
    bio: state => state.user.end_user.bio,
    companyWebsite: state => state.user.website.company,
    personalWebsite: state => state.user.website.personal,
    dateOfBirth: state => state.user.end_user.date_of_birth,
    gender: state => state.user.end_user.gender,
    city: state => state.user.end_user.city,
    country: state => state.user.end_user.country,
    avatar: state => state.user.avatar,
    title: state => state.user.end_user.title,
    customTitle: state => state.customTitle,
    isDarkMode: state => state.settings.is_dark_mode,
    isEnabledNotification: state => state.settings.enabled_notification,
    isUserUnsaved (state) {
      const user = UserState.collectUser()
      return !(
        isEqual(user.avatar, state.user.avatar) &&
        isEqual(user.first_name, state.user.first_name) &&
        isEqual(user.last_name, state.user.last_name) &&
        isEqual(user.username, state.user.username) &&
        isEqual(user.email, state.user.email) &&
        isEqual(user.end_user.bio, state.user.end_user.bio) &&
        isEqual(user.website.company, state.user.website.company) &&
        isEqual(user.website.personal, state.user.website.personal) &&
        isEqual(user.end_user.date_of_birth, state.user.end_user.date_of_birth) &&
        isEqual(user.end_user.gender, state.user.end_user.gender) &&
        isEqual(user.end_user.city, state.user.end_user.city) &&
        isEqual(user.end_user.country, state.user.end_user.country) &&
        isEqual(user.end_user.title, state.user.end_user.title)
      )
    }
  }
}
