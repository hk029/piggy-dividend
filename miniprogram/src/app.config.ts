export default defineAppConfig({
  pages: [
    'pages/home/index',
    'pages/ledger/index',
    'pages/calendar/index',
    'pages/asset/index',
    'pages/mine/index',
  ],
  tabBar: {
    color: '#6F756B',
    selectedColor: '#C93A2E',
    backgroundColor: '#FFFDF8',
    borderStyle: 'white',
    list: [
      { pagePath: 'pages/home/index', text: '首页', iconPath: 'assets/tabbar/home.png', selectedIconPath: 'assets/tabbar/home-active.png' },
      { pagePath: 'pages/ledger/index', text: '账本', iconPath: 'assets/tabbar/book.png', selectedIconPath: 'assets/tabbar/book-active.png' },
      { pagePath: 'pages/calendar/index', text: '日历', iconPath: 'assets/tabbar/calendar.png', selectedIconPath: 'assets/tabbar/calendar-active.png' },
      { pagePath: 'pages/asset/index', text: '资产', iconPath: 'assets/tabbar/pie.png', selectedIconPath: 'assets/tabbar/pie-active.png' },
      { pagePath: 'pages/mine/index', text: '我的', iconPath: 'assets/tabbar/mine.png', selectedIconPath: 'assets/tabbar/mine-active.png' },
    ],
  },
  window: {
    backgroundTextStyle: 'light',
    navigationBarBackgroundColor: '#FFF9ED',
    navigationBarTitleText: '小猪攒息',
    navigationBarTextStyle: 'black',
  },
})
